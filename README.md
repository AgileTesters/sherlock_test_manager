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
---

### You can use either pipenv or venv to manage your python virtual enviroment.

Setup python with pipenv:
> note that pipenv us currently not working on macOs big sur

install
```
pip3 install pipenv OR brew install pipenv
```
access sherlock_backend and run:

```
pipenv install
pipenv run flask run
```

#### OR

Setup python with virtualenv:
more info: https://virtualenv.pypa.io/en/latest/user_guide.html#

```
pip3 install virtualenv
```

navigate to the sherlockback project folder and run:

```
virtualenv sherlock_python_env
```

after that, you need to activate your virtualenv. run:

```
source sherlock_python_env/bin/activate
```
the code above works for mac OR linux.
to run this with windows, you can do `.\_env\Scripts\activate`

once you see the virtual environment like this `(sherlock_python_env)`on your terminal you can run:

```
pip install -r requirements.txt
flask run
```

you can run `deactive` any time to leave the virtualenv

---


setup vue:
```
npm install
npm run serve
```