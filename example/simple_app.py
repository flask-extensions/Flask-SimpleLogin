from flask import Flask, jsonify, render_template
from flask.views import MethodView

from collections import namedtuple

import sys
sys.path.append(".")
from flask_simplelogin import SimpleLogin, get_username, login_required

my_users = {
    'chuck': {'password': 'norris', 'roles': ['admin']},
    'lee': {'password': 'douglas', 'roles': []},
    'mary': {'password': 'jane', 'roles': []},
    'steven': {'password': 'wilson', 'roles': ['admin']}
}
Message=namedtuple("Message", "message category")
messages = {
    'login_success': Message('login success!', 'danger'),
    'login_failure': Message('invalid credentials','success'),
    'is_logged_in': Message('already logged in','primary'),
    'logout': Message('Logged out!','primary'),
    'login_required': Message('You need to login first','success'),
    'access_denied': 'Access Denied',
    'auth_error': 'Authentication Error: {0}',
}

def check_my_users(user):
    """Check if user exists and its credentials.
    Take a look at encrypt_app.py and encrypt_cli.py
     to see how to encrypt passwords
    """
    user_data = my_users.get(user['username'])
    if not user_data:
        return False  # <--- invalid credentials
    elif user_data.get('password') == user['password']:
        return True  # <--- user is logged in!

    return False  # <--- invalid credentials


app = Flask(__name__)
app.config.from_object('settings')

SimpleLogin(app, login_checker=check_my_users, messages=messages)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/secret')
@login_required(username=['chuck', 'mary'])
def secret():
    return render_template('secret.html')


@app.route('/api', methods=['POST'])
@login_required(basic=True)
def api():
    return jsonify(data='You are logged in with basic auth')


def be_admin(username):
    """Validator to check if user has admin role"""
    user_data = my_users.get(username)
    if not user_data or 'admin' not in user_data.get('roles', []):
        return "User does not have admin role"


def have_approval(username):
    """Validator: all users approved, return None"""
    return


@app.route('/complex')
@login_required(must=[be_admin, have_approval])
def complexview():
    return render_template('secret.html')


class ProtectedView(MethodView):
    decorators = [login_required]

    def get(self):
        return "You are logged in as <b>{0}</b>".format(get_username())


app.add_url_rule('/protected', view_func=ProtectedView.as_view('protected'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, use_reloader=True, debug=True)
