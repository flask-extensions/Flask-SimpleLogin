import pytest
from flask import Flask
from flask_simplelogin import SimpleLogin, Message


class Settings(dict):
    """A dictionary-like object that allows access to its values using the
    attribute syntax (as required by Flask.config.from_object)"""

    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)
        for key, value in kwargs.items():
            self.__dict__[key] = value


def create_simple_login(settings):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret-here"
    app.config.from_object(settings)
    return SimpleLogin(app)


def test_default_configs_are_loaded(app):
    settings = Settings()
    sl = create_simple_login(settings)
    assert sl.config["blueprint"] == "simplelogin"
    assert sl.config["login_url"] == "/login/"
    assert sl.config["logout_url"] == "/logout/"
    assert sl.config["home_url"] == "/"


def test_custom_configs_are_loaded(app):
    settings = Settings(
        SIMPLELOGIN_BLUEPRINT="custom_blueprint",
        SIMPLELOGIN_LOGIN_URL="/custom_login/",
        SIMPLELOGIN_LOGOUT_URL="/custom_logout/",
        SIMPLELOGIN_HOME_URL="/custom_home/",
    )
    sl = create_simple_login(settings)
    assert sl.config["blueprint"] == "custom_blueprint"
    assert sl.config["login_url"] == "/custom_login/"
    assert sl.config["logout_url"] == "/custom_logout/"
    assert sl.config["home_url"] == "/custom_home/"


def test_configs_are_loaded_with_backwards_compatibility(client):
    settings = Settings(
        SIMPLE_LOGIN_BLUEPRINT="custom_blueprint",
        SIMPLE_LOGIN_LOGIN_URL="/custom_login/",
        SIMPLE_LOGIN_LOGOUT_URL="/custom_logout/",
        SIMPLE_LOGIN_HOME_URL="/custom_home/",
    )
    with pytest.warns(FutureWarning):
        sl = create_simple_login(settings)
    assert sl.config["blueprint"] == "custom_blueprint"
    assert sl.config["login_url"] == "/custom_login/"
    assert sl.config["logout_url"] == "/custom_logout/"
    assert sl.config["home_url"] == "/custom_home/"


def test_custom_messages():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret-here"
    messages = {
        "login_success": Message("customized login message", category="login_success"),
        "is_logged_in": "all set",
        "logout": None,
    }

    sl = SimpleLogin(app, messages=messages)
    assert sl.messages["login_success"] == messages["login_success"]
    assert isinstance(sl.messages["is_logged_in"], Message)
    assert sl.messages["logout"] is None
    assert sl.messages["login_required"] == SimpleLogin.messages["login_required"]
