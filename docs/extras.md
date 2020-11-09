# Extras

## Do you need Access Control?

You can easily mix Flask Simple Login with[Flask-Allows](https://github.com/justanr/flask-allows):

```console
$ pip install flask_allows
```

And then:

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

## Need JSON Web Token (JWT) support?

Take a look at [Flask-JWT-Simple](https://github.com/vimalloc/flask-jwt-simple) and of course you can mix it with Flask Simple Login.

Alternatives:

- [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
- [Flask-User](https://github.com/lingthio/Flask-User)
- [Flask-Security](https://pythonhosted.org/Flask-Security/)
- [Flask-Principal](https://pythonhosted.org/Flask-Principal/)

Those extensions are really complete and <b>production ready</b>!