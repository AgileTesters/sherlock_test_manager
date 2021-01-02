Sherlock v2

> WIP - not suitable for production.


Setting up your development env
---

Tech menu:
- docker: last version
  - last version mariadb container
- pipenv: last version (python 3.9++) (doesnt work with macOs big sur)
- node: at least v14


---
Setup database:

```
docker pull mariadb
docker run --name mariadbdev -p 3306:3306 -e MYSQL_ROOT_PASSWORD=12345 -d mariadb
docker start mariadbdev
```
Setup python:

```
pip3 install pipenv OR brew install pipenv
```
access sherlock_backend and run:

```
pipenv install
pipenv run flask run
```

setup vue:
```
npm install
npm run serve
```