import pytest
from flask import Flask, jsonify, render_template
from flask.views import MethodView
from flask_simplelogin import SimpleLogin
from flask_simplelogin import login_required
from flask_simplelogin import get_username


@pytest.fixture
def app():
    """Flask Pytest uses it"""
    myapp = Flask(__name__)
    myapp.config["SECRET_KEY"] = "secret-here"
    SimpleLogin(myapp)

    @myapp.route("/secret")
    @login_required
    def secret():
        return "This is Safe"

    @myapp.route("/username_required")
    @login_required(username=["user1", "user2"])
    def username_required():
        return "This is Safe"

    @myapp.route("/api", methods=["POST"])
    @login_required(basic=True)
    def api():
        return jsonify(data="You are logged in with basic auth")

    def be_admin(username):
        """Validator to check if user has admin role"""
        if username != "admin":
            return "User does not have admin role"

    def have_approval(username):
        """Validator: all users approved, return None"""
        return

    @myapp.route("/complex")
    @login_required(must=[be_admin, have_approval])
    def complexview():
        return render_template("secret.html")

    class ProtectedView(MethodView):
        decorators = [login_required]

        def get(self):
            return "You are logged in as <b>{0}</b>".format(get_username())

    myapp.add_url_rule("/protected", view_func=ProtectedView.as_view("protected"))

    return myapp
