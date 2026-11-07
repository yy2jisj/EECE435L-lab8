# EECE 435L Lab 8

Youssef Al Hajj Youness · AUB username `yaa49`

## Activity 1

The Flask app returns `Hello, World!` at `GET /`. Start Docker Desktop in Linux container mode and run these commands from this directory in PowerShell.

```powershell
docker build -t flask_docker ./activity1
docker run -d --name lab8-hello -p 127.0.0.1:5000:5000 flask_docker
curl.exe -fsS -i http://127.0.0.1:5000/
python ./verify.py activity1
docker ps -a
docker stop lab8-hello
docker logs lab8-hello
```

Open `Activity1_Report.docx` for the command screenshots and explanations. Stop `lab8-hello` before starting Activity 2 because both the Hello World container and the first Lab 5 image use host port 5000.

## Activity 2

Both versions use the Flask API and SQLite database from the original [Lab 5 repository](https://github.com/yy2jisj/Lab5-Postman-APIs/tree/c796e7b847b4d4d206f3aaeac4da3f69678d70ef). Version 0.0.1 preserves the Lab 5 routes and binds the server inside the container on port 5000. Version 0.0.2 also exposes `GET /get_users` on port 3000 and returns a JSON array of names selected from the SQLite `users` table in user ID order.

```powershell
$repo = 'yaa49/lab8-youssef_al_hajj_youness'
docker build -t "${repo}:0.0.1.RELEASE" ./activity2/0.0.1
docker build -t "${repo}:0.0.2.RELEASE" ./activity2/0.0.2
docker run -d --name lab8-v1 -p 127.0.0.1:5000:5000 "${repo}:0.0.1.RELEASE"
docker run -d --name lab8-v2 -p 127.0.0.1:3000:3000 "${repo}:0.0.2.RELEASE"
docker ps --filter name=lab8-
docker logs lab8-v1
docker logs lab8-v2
curl.exe -fsS -i http://127.0.0.1:5000/api/users
curl.exe -fsS -i http://127.0.0.1:3000/get_users
python ./verify.py activity2
```

The database ships with the two sample records from Lab 5. The verification script compares the names API with a separate SQLite query inside the running container and checks that the response changes after inserting and deleting a temporary record. It also exercises the original Lab 5 create, read, update, and delete routes on port 5000.

## Verified results

| Check | Result |
| --- | --- |
| Hello World on port 5000 | HTTP 200 and `Hello, World!` |
| Lab 5 API on port 5000 | HTTP 200 and both original records. The create, read, update, and delete check passed. |
| `GET /get_users` on port 3000 | HTTP 200 and `["John Doe","Maya Haddad"]`. The response matched the database and followed a temporary insert and delete. |

## Submission checklist

The Word report, in-app screenshots, and Moodle ZIP are kept locally for review.

- [x] Activity 1 Word report with real screenshots and explanations for `docker ps -a`, `docker stop`, and `docker logs`.
- [x] Activity 2 Docker Desktop screenshot showing both image names and tags.
- [x] Activity 2 screenshots of the running containers, both HTTP responses, and passing tests.
- [x] Source, Dockerfiles, dependencies, and SQLite databases for both versions.
- [x] ZIP with the code and evidence for Moodle.
