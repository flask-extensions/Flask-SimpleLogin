# Configuring

Simple way

~~~python
from flask import Flask
from flask_simplelogin import SimpleLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'
app.config['SIMPLELOGIN_USERNAME'] = 'chuck'
app.config['SIMPLELOGIN_PASSWORD'] = 'norris'

SimpleLogin(app)
~~~

That works, but is not so clever, lets use env vars.

~~~
$ export SIMPLELOGIN_USERNAME=chuck
$ export SIMPLELOGIN_PASSWORD=norris
~~~

then SimpleLogin will read those env vars automatically.

~~~python
from flask import Flask
from flask_simplelogin import SimpleLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'
SimpleLogin(app)
~~~

But what if you have more users and more complex auth logic? <b>Write a custom login checker.</b>

## Using a custom login checker

`SimpleLogin` automatically loads Flask configurations prefixed with `SIMPLELOGIN_`, thus to set a custom login, logout or home URL:

~~~python
from flask import Flask
from flask_simplelogin import SimpleLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'
app.config['SIMPLELOGIN_LOGIN_URL'] = '/signin/'
app.config['SIMPLELOGIN_LOGOUT_URL'] = '/exit/'
app.config['SIMPLELOGIN_HOME_URL'] = '/en/'

SimpleLogin(app)
~~~

## Encrypt passwords

You can use the from `werkzeug.security import check_password_hash, generate_password_hash` utilities to encrypt passwords.

A working example is available in `manage.py` of [example app](https://github.com/flask-extensions/flask_simplelogin/tree/master/example)