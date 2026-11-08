# EECE 435L Lab 8 Docker and Containers

Youssef Al Hajj Youness · AUB username `yaa49`

Start Docker Desktop in Linux container mode. Run the PowerShell commands from this folder.

## Activity 1

The Flask app in `activity1/` returns `Hello, World!` on port 5000.

```powershell
docker build -t flask_docker ./activity1
docker run --init -d --name lab8-hello -p 127.0.0.1:5000:5000 flask_docker
curl.exe -fsS -i http://127.0.0.1:5000/
docker ps -a
docker stop lab8-hello
docker logs lab8-hello
```

The Word report explains the three Docker commands and shows their output. Stop the Hello World container before running Activity 2.

## Activity 2

| Image | Port | Endpoint |
| --- | --- | --- |
| `yaa49/lab8-youssef_al_hajj_youness:0.0.1.RELEASE` | 5000 | `GET /api/users` and the Lab 5 CRUD routes |
| `yaa49/lab8-youssef_al_hajj_youness:0.0.2.RELEASE` | 3000 | `GET /get_users` and the Lab 5 CRUD routes |

Both builds use the same API source and SQLite database from the [original Lab 5 repository](https://github.com/yy2jisj/Lab5-Postman-APIs/tree/c796e7b847b4d4d206f3aaeac4da3f69678d70ef). Each container gets its own copy of the database. The port 3000 endpoint selects names in user ID order.

```powershell
$image = 'yaa49/lab8-youssef_al_hajj_youness'
docker build -t "${image}:0.0.1.RELEASE" ./activity2
docker build -f ./activity2/Dockerfile.users -t "${image}:0.0.2.RELEASE" ./activity2
docker run --init -d --name lab8-v1 -p 127.0.0.1:5000:5000 "${image}:0.0.1.RELEASE"
docker run --init -d --name lab8-v2 -p 127.0.0.1:3000:3000 "${image}:0.0.2.RELEASE"
curl.exe -fsS -i http://127.0.0.1:5000/api/users
curl.exe -fsS -i http://127.0.0.1:3000/get_users
python ./verify.py activity2
```

Both requests returned HTTP 200. The first returned the two Lab 5 records. The second returned `["John Doe","Maya Haddad"]`. The verification script checks CRUD on port 5000 and compares the names response with SQLite before and after a temporary insert and delete.

## Submission files

The local Moodle ZIP includes the Word report, both activities’ source files, and the Activity 2 captures in `screenshots/`. The Activity 1 captures are embedded in the report. The report, screenshots, and ZIP are kept locally for review.
