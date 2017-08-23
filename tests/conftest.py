import pytest
from flask import Flask
from flask_simplelogin import SimpleLogin
from flask_simplelogin import login_required


@pytest.fixture
def app():
    """Flask Pytest uses it"""
    myapp = Flask(__name__)
    myapp.config['SECRET_KEY'] = 'secret-here'
    SimpleLogin(myapp)

    @myapp.route('/secret')
    @login_required
    def secret():
        return "This is Safe"

    return myapp
