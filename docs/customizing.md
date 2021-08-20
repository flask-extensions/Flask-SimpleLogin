# Customizing

## Customizing templates

There are only one template to customize and it is called `login.html`.
Example is:

```python
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

Take a look at the [example app](https://github.com/flask-extensions/flask_simplelogin/tree/main/example).

And you can customize it in anyway you want and need, it receives a `form` in the context and it is a WTForms form. The submit should be done to `request.path` which is the same as the login view.

You can also use `{% if is_logged_in() %}` in your template if needed.

## Customizing or translating message alerts

The default message alerts are:

| Key | Message | 
|---|---|
| `login_success` | login success! |
| `login_failure` | invalid credentials |
| `is_logged_in` | already logged in |
| `logout` | Logged out! |
| `login_required` | You need to login first |
| `access_denied` | Access Denied |
| `auth_error` | Authentication Error: `{0}` |

NOTE: the `{0}` in the authentication_error is a required place holder to pass in the validator error message.

```python
app = Flask(__name__)
messages = {
    'login_success': 'Você está dentro!',
    'login_failure': 'ungültige Anmeldeinformationen',
    'is_logged_in': 'Iam initium',
    'logout': 'Déconnecté!',
    'login_required': 'Devi prima accedere',
    'access_denied': 'Acceso denegado',
    'auth_error': '授權錯誤： {0}'
}
SimpleLogin(app, messages=messages)
```

## Custom validators

When you pass the `must` argument to `login_required` decorator, it can be a function or a list of functions. If function returns `None`, it means **no** error and validation passed. If function returns an error message (stringt), it means validation failed.

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

Take a look at the [example app](https://github.com/flask-extensions/flask_simplelogin/tree/main/example).
