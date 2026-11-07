import argparse
import json
import subprocess
from urllib.request import Request, urlopen


def http(port, path, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    request = Request(
        f"http://127.0.0.1:{port}{path}",
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method=method,
    )
    with urlopen(request, timeout=10) as response:
        assert response.status == 200, f"{method} {path} returned {response.status}"
        assert response.headers.get_content_type() == "application/json"
        return json.load(response)


def docker(*args):
    return subprocess.check_output(["docker", *args], text=True).strip()


def assert_running(container, port):
    assert docker("inspect", "--format", "{{.State.Status}}", container) == "running"
    assert f"127.0.0.1:{port}" in docker("port", container, f"{port}/tcp")


def db_names(container):
    query = (
        "import json, sqlite3; "
        "db = sqlite3.connect('file:/app/database.db?mode=ro', uri=True); "
        "print(json.dumps([row[0] for row in db.execute("
        "'SELECT name FROM users ORDER BY user_id')]))"
    )
    return json.loads(docker("exec", container, "python", "-c", query))


def test_activity1():
    assert_running("lab8-hello", 5000)
    with urlopen("http://127.0.0.1:5000/", timeout=10) as response:
        assert response.status == 200
        assert response.read().decode() == "Hello, World!"
    print("PASS  Activity 1 GET :5000/ returned HTTP 200 and Hello, World!")


def test_v1():
    container = "lab8-v1"
    port = 5000
    assert_running(container, port)
    baseline = http(port, "/api/users")
    assert len(baseline) >= 1
    assert [row["name"] for row in baseline] == db_names(container)
    assert http(port, f"/api/users/{baseline[0]['user_id']}") == baseline[0]
    print(f"PASS  v0.0.1 GET :5000/api/users and GET by ID returned {len(baseline)} original rows")

    sample = {
        "name": "Lab 8 Verification",
        "email": "lab8-verification@example.com",
        "phone": "00000000",
        "address": "Test address",
        "country": "Lebanon",
    }
    created = http(port, "/api/users/add", "POST", sample)
    user_id = created["user_id"]
    try:
        assert created == dict(sample, user_id=user_id)
        updated = dict(created, name="Lab 8 Verification Updated")
        assert http(port, "/api/users/update", "PUT", updated) == updated
        assert http(port, f"/api/users/{user_id}") == updated
    finally:
        deleted = http(port, f"/api/users/delete/{user_id}", "DELETE")
    assert deleted["status"] == "User deleted successfully"
    assert http(port, "/api/users") == baseline
    print("PASS  v0.0.1 POST, PUT, GET and DELETE round trip restored the baseline")


def test_v2():
    container = "lab8-v2"
    port = 3000
    assert_running(container, port)
    baseline = db_names(container)
    assert len(baseline) >= 1
    assert http(port, "/get_users") == baseline
    print(f"PASS  v0.0.2 GET :3000/get_users returned HTTP 200 and {json.dumps(baseline)}")
    print("PASS  Response matched a separate SQLite SELECT in the running container")

    created = http(
        port,
        "/api/users/add",
        "POST",
        {
            "name": "Lab 8 Database Check",
            "email": "lab8-db-check@example.com",
            "phone": "00000000",
            "address": "Test address",
            "country": "Lebanon",
        },
    )
    try:
        expected = baseline + [created["name"]]
        assert http(port, "/get_users") == db_names(container) == expected
    finally:
        http(port, f"/api/users/delete/{created['user_id']}", "DELETE")
    assert http(port, "/get_users") == db_names(container) == baseline
    print("PASS  /get_users reflected insertion and deletion of a temporary database row")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", choices=("activity1", "v1", "v2", "activity2"))
    target = parser.parse_args().target
    if target == "activity1":
        test_activity1()
    if target in ("v1", "activity2"):
        test_v1()
    if target in ("v2", "activity2"):
        test_v2()
