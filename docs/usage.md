# Usage

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

## Protecting Flask Admin views

```python
from flask_admin.contrib.foo import ModelView
from flask_simplelogin import is_logged_in


class AdminView(ModelView)
    def is_accessible(self):
        return is_logged_in('admin')
```