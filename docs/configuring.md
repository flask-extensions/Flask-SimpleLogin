# Configuring

Simplest way:

```python
from flask import Flask
from flask_simplelogin import SimpleLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'
app.config['SIMPLELOGIN_USERNAME'] = 'chuck'
app.config['SIMPLELOGIN_PASSWORD'] = 'norris'

SimpleLogin(app)
```

That works, but is not so clever, let's use environment variables:

```console
$ export SIMPLELOGIN_USERNAME=chuck
$ export SIMPLELOGIN_PASSWORD=norris
```

Now Simple Login will read and use them automatically:

```python
from flask import Flask
from flask_simplelogin import SimpleLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'
SimpleLogin(app)
```

But what if you have more users and more complex authentication logic?

## Using a custom login checker

```python
from flask import Flask
from flask_simplelogin import SimpleLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'


def only_chuck_norris_can_login(user):
    """:param user: dict {'username': 'foo', 'password': 'bar'}"""
    if user.get('username') == 'chuck' and user.get('password') == 'norris':
       return True  # <--- Allowed
    return False  # <--- Denied


SimpleLogin(app, login_checker=only_chuck_norris_can_login)
```

## Using a custom login, logout or home URL

Simple Login automatically loads Flask configurations prefixed with `SIMPLELOGIN_`, thus to set a custom login, logout or home URL:

```python
from flask import Flask
from flask_simplelogin import SimpleLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'
app.config['SIMPLELOGIN_LOGIN_URL'] = '/signin/'
app.config['SIMPLELOGIN_LOGOUT_URL'] = '/exit/'
app.config['SIMPLELOGIN_HOME_URL'] = '/en/'

SimpleLogin(app)
```

## Encrypting passwords

You can use the `from werkzeug.security import check_password_hash, generate_password_hash` utilities to encrypt passwords.

A working example is available in `manage.py` of [example app](https://github.com/flask-extensions/flask_simplelogin/tree/main/example)
