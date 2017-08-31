[![Travis](https://img.shields.io/travis/rochacbruno/flask_simplelogin.svg?style=flat-square)](https://travis-ci.org/rochacbruno/flask_simplelogin)
[![PyPI](https://img.shields.io/pypi/v/flask_simplelogin.svg?style=flat-square)](https://pypi.org/project/flask_simplelogin/)
[![PyPI versions](https://img.shields.io/pypi/pyversions/flask_simplelogin.svg?style=flat-square)](https://pypi.org/project/flask_simplelogin/)
[![PyPI formats](https://img.shields.io/pypi/format/flask_simplelogin.svg?style=flat-square)](https://pypi.org/project/flask_simplelogin/)
[![Flask](https://img.shields.io/badge/Flask-Extension-blue.svg?style=flat-square)](https://github.com/pallets/flask)

# Login Extension for Flask

There are other good and recommended options to deal with web authentication & authorization
in Flask.

**I recommend you to use:**

- [Flask-Login](https://flask-login.readthedocs.io)
- [Flask-User](https://github.com/lingthio/Flask-User)
- [Flask-Security](https://pythonhosted.org/Flask-Security/)
- [Flask-Principal](https://pythonhosted.org/Flask-Principal/)

Those extensions are really complete and **production ready**!

## So why **Flask Simple Login**?

However sometimes you need something **simple** for that small project or for
prototyping.

## Flask Simple Login

What it provides:

- Login and Logout forms and pages
- Function to check if user is logged-in
- Decorator for views
- Easy and customizable `login_checker`
- Basic-Auth for API endpoints

What it does not provide:

- ~~Database Integration~~
- ~~Password management~~
- ~~API authentication with Token or JWT~~
- ~~Role or user based access control~~

> of course you can easily implement all above by your own. Take a look at [example](/example).

## Hot it works

First install it from [PyPI](https://pypi.org/project/flask_simplelogin/).

> `pip install flask_simplelogin`

```python
from flask import Flask
from flask_simplelogin import SimpleLogin

app = Flask(__name__)
SimpleLogin(app)
```

## **That's it!**

Now you have `/login` and `/logout` routes in your application.

The username defaults to `admin` and the password defaults to `secret` (yeah that's not clever, let's see how to change it)


![Login Screen](/login_screen.png)


## Configuring

Simple way

```python
from flask import Flask
from flask_simplelogin import SimpleLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'
app.config['SIMPLELOGIN_USERNAME'] = 'chuck'
app.config['SIMPLELOGIN_PASSWORD'] = 'norris'

SimpleLogin(app)
```

That works, but is not so clever, lets use env vars.

```bash
$ export SIMPLELOGIN_USERNAME=chuck
$ export SIMPLELOGIN_PASSWORD=norris
```

then `SimpleLogin` will read those env vars automatically.

```python
from flask import Flask
from flask_simplelogin import SimpleLogin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'
SimpleLogin(app)
```

But what if you have more users and more complex auth logic?
**write a custom login checker**

### Using a custom login checker

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

### Encrypt passwords

You can use the `from werkzeug.security import check_password_hash, generate_password_hash`
utilities to encrypt passwords.

A working example is available in `manage.py` of [example app](https://github.com/rochacbruno/flask_simplelogin/blob/master/example/)


## Checking if user is logged in

```python

from flask_simplelogin import is_logged_in

if is_logged_in():
    # do things if anyone is logged in

if is_logged_in('admin'):
    # do things only if admin is logged in
```


## Protecting your views

```python
from flask_simplelogin import login_required

@app.route('/it_is_protected')
@login_required  # < --- simple decorator
def foo():
    return 'secret'

@app.route('/only_mary_can_access')
@login_required(username='mary')  # < --- accepts a list of names
def bar():
    return "Mary's secret"

@app.route('/api', methods=['POST'])
@login_required(basic=True)  # < --- Basic HTTP Auth for API
def api():
    # curl -XPOST localhost:5000/api -H "Authorization: Basic Y2h1Y2s6bm9ycmlz" -H "Content-Type: application/json"
    # Basic-Auth takes base64 encripted username:password
    return jsonify(data='You are logged in with basic auth')

class ProtectedView(MethodView):  # < --- Class Based Views
    decorators = [login_required]
    def get(self):
        return "only loged in users can see this"
```

### Protecting Flask Admin views

```python

from flask_admin.contrib.foo import ModelView
from flask_simplelogin import is_logged_in


class AdminView(ModelView)
    def is_accessible(self):
        return is_logged_in('admin')
```

## Customizing templates

There are only one template to customize and it is called `login.html`

Example is:

```html
{% extends 'base.html' %}
{% block title %}Login{% endblock %}
{% block messages %}
   {{super()}}
   {%if form.errors %}
     <ul class="alert alert-danger">
       {% for field, errors in form.errors.items() %}
         <li>{{field}} {% for error in errors %}{{ error }}{% endfor %}</li>
       {% endfor %}
     </ul>
   {% endif %}
{% endblock %}

{% block page_body %}
       <form action="{{ url_for('simplelogin.login', next=request.args.get('next', '/')) }}" method="post">
            <div class="form-group">
            {{ form.csrf_token }}
            {{form.username.label}}<div class="form-control">{{ form.username }}</div><br>
            {{form.password.label}}<div class="form-control"> {{ form.password }}</div><br>
            </form>
           <input type="submit" value="Send">
       </form>
{% endblock %}
```

> Take a look at the [example app](https://github.com/rochacbruno/flask_simplelogin/blob/master/example/).

And you can customize it in anyway you want and need, it receives a `form` in context and it is a `WTF form` the submit should be done to `request.path` which is the same `/login` view.

You can also use `{% if is_logged_in %}` in your template if needed.

## Customizing message alerts

```python
app = Flask(__name__)
messages = {
    'login_success': 'Great You are in!!',
    'login_failure': 'Credenciais inválidas :(',
    'is_logged_in': 'You dont need to login again!',
    'logout': 'Bye Bye!'
}
SimpleLogin(app, messages=messages)
```

## Custom validators

Pass `must` argument to `login_required` decorator, it can be a `function` or a list of `functions` if function returns `None` means **No** error and validator passed. if function returns an `"Error message"` means validator did not passed.

```python
def be_admin(username):
    """Validator to check if user has admin role"""
    user_data = my_users.get(username)
    if not user_data or 'admin' not in user_data.get('roles', []):
        return "User does not have admin role"


def have_approval(username):
    """Validator: all users approved so return None"""
    return


@app.route('/protected')
@login_required(must=[be_admin, have_approval])
def protected():
    return render_template('secret.html')

```

> Take a look at the [example app](https://github.com/rochacbruno/flask_simplelogin/blob/master/example/).

## Requirements

- Flask-WTF and WTForms
- `SECRET_KEY` set in your `app.config`

## Integrations

### Do you need Access Control? you can easily mix `flask_simplelogin` with `flask_allows`

https://github.com/justanr/flask-allows
`pip install flask_allows`

```python
from flask import Flask, g
from flask_simplelogin import SimpleLogin
from flask_allows import Allows

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something-secret'


def is_staff(ident, request):
    return ident.permlevel == 'staff'

def only_chuck_norris_can_login(user):
    if user.get('username') == 'chuck' and user.get('password') == 'norris':
       # Bind the logged in user data to the `g` global object
       g.user.username = user['username']
       g.user.permlevel = 'staff'  # set user permission level
       return True  # Allowed
    return False  # Denied

# init allows
allows = Allows(identity_loader=lambda: g.user)

# init SimpleLogin
SimpleLogin(app, login_checker=only_chuck_norris_can_login)

# a view which requires a logged in user to be member of the staff group
@app.route('/staff_only')
@allows.requires(is_staff)
@login_required
def a_view():
    return "staff only can see this"

```

### Need JSON Web Token (JWT)?

Take a look at [Flask-JWT-Simple](https://github.com/vimalloc/flask-jwt-simple) and of course you can mix SimpleLogin + JWT Simple
