"""Flask Simple Login - Login Extension for Flask"""

__author__ = "Bruno Rocha"
__email__ = "rochacbruno@gmail.com"


import logging
import os
from functools import wraps
from typing import Callable, Iterable, Mapping, TypedDict
from urllib.parse import urljoin, urlparse
from uuid import uuid4
from warnings import warn

from flask import (
    Blueprint,
    Flask,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask.typing import ResponseReturnValue
from flask_wtf import FlaskForm, Form  # type: ignore
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired

logger = logging.getLogger(__name__)


class User(TypedDict):
    username: str | None
    password: str | None


Validator = Callable[[str | None], str | None]
LoginChecker = Callable[[User], bool]


class Message:
    def __init__(self, text: str, category: str = "primary"):
        self.text = text
        self.category = category

    @classmethod
    def from_current_app(cls, label: str) -> "Message":
        """Helper to get messages from Flask's current_app"""
        return current_app.extensions["simplelogin"].messages.get(label)

    def __str__(self) -> str:
        return self.text

    def format(self, *args, **kwargs) -> str:
        return self.text.format(*args, **kwargs)


class LoginForm(FlaskForm):
    "Default login form"

    username = StringField(
        "name", validators=[DataRequired()], render_kw={"autocapitalize": "none"}
    )
    password = PasswordField("password", validators=[DataRequired()])


def default_login_checker(user: User) -> bool:
    """User must be a dictionary here default is checking username/password
    if login is ok returns True else False

    :param user: dict {'username':'', 'password': ''}
    """
    username = user.get("username")
    password = user.get("password")
    the_username = os.environ.get(
        "SIMPLELOGIN_USERNAME", current_app.config.get("SIMPLELOGIN_USERNAME", "admin")
    )
    the_password = os.environ.get(
        "SIMPLELOGIN_PASSWORD", current_app.config.get("SIMPLELOGIN_PASSWORD", "secret")
    )
    return username == the_username and password == the_password


def is_logged_in(username: str | Iterable[str] | None = None) -> bool:
    """Checks if user is logged in if `username` is passed check if specified
    user is logged in username can be a list"""
    if username:
        if isinstance(username, str):
            username = (username,)
            got = get_username()
        return (
            "simple_logged_in" in session and isinstance(got, str) and got in username
        )
    return "simple_logged_in" in session


def get_username() -> str | None:
    """Get current logged in username"""
    return session.get("simple_username")


def login_required(
    function: Callable | None = None,
    username: str | Iterable[str] | None = None,
    basic: bool = False,
    must: Iterable[Validator] | None = None,
):
    """Decorate views to require login
    @login_required
    @login_required()
    @login_required(username='admin')
    @login_required(username=['admin', 'jon'])
    @login_required(basic=True)
    @login_required(must=[function, another_function])
    """

    if function and not callable(function):
        raise ValueError(
            "Decorator receives only named arguments, "
            'try login_required(username="foo")'
        )

    def check(
        validators: Validator | Iterable[Validator] | None,
    ) -> tuple[str, int] | None:
        """Return in the first validation error, else return None"""
        if validators is None:
            return None

        if callable(validators):
            validators = (validators,)

        for validator in validators:
            error = validator(get_username())
            if error is not None:
                return Message.from_current_app("auth_error").format(error), 403

        return None

    def dispatch(
        fun: Callable[..., ResponseReturnValue], *args, **kwargs
    ) -> ResponseReturnValue:
        if basic and request.is_json:
            return dispatch_basic_auth(fun, *args, **kwargs)

        if is_logged_in(username=username):
            return check(must) or fun(*args, **kwargs)
        elif is_logged_in():
            return Message.from_current_app("access_denied").text, 403
        else:
            SimpleLogin.flash("login_required")
            return redirect(url_for("simplelogin.login", next=request.path))

    def dispatch_basic_auth(
        fun: Callable[..., ResponseReturnValue], *args, **kwargs
    ) -> ResponseReturnValue:
        simplelogin = current_app.extensions["simplelogin"]
        auth_response = simplelogin.basic_auth()
        if auth_response is True:
            return check(must) or fun(*args, **kwargs)
        else:
            return auth_response

    if function:

        @wraps(function)
        def simple_decorator(*args, **kwargs) -> ResponseReturnValue:
            """This is for when decorator is @login_required"""
            return dispatch(function, *args, **kwargs)

        return simple_decorator

    def decorator(f):
        """This is for when decorator is @login_required(...)"""

        @wraps(f)
        def wrap(*args, **kwargs) -> ResponseReturnValue:
            return dispatch(f, *args, **kwargs)

        return wrap

    return decorator


class SimpleLoginNotInitializedError(Exception):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            "SimpleLogin is not initialized, use `SimpleLogin.init_app(app)`"
        )


class SimpleLogin:
    """Simple Flask Login"""

    messages = {
        "login_success": Message("login success!", "success"),
        "login_failure": Message("invalid credentials", "danger"),
        "is_logged_in": Message("already logged in"),
        "logout": Message("Logged out!"),
        "login_required": Message("You need to login first", "warning"),
        "access_denied": Message("Access Denied"),
        "auth_error": Message("Authentication Error: {0}"),
    }

    @staticmethod
    def flash(label: str, *args, **kwargs) -> None:
        msg = Message.from_current_app(label)
        if not msg:
            return

        if args or kwargs:
            flash(msg.format(*args, **kwargs), msg.category)
        else:
            flash(msg.text, msg.category)

    def __init__(
        self,
        app: Flask | None = None,
        login_checker: LoginChecker | None = None,
        login_form: Form = None,
        messages: Mapping[str, Message] | None = None,
    ):
        self.config = {
            "blueprint": "simplelogin",
            "login_url": "/login/",
            "logout_url": "/logout/",
            "home_url": "/",
        }
        self.app: Flask | None = None
        self._login_checker = login_checker or default_login_checker
        self._login_form = login_form or LoginForm
        self.on_logout_callbacks: list[Callable] = []
        if app is not None:
            self.init_app(
                app=app,
                login_checker=login_checker,
                login_form=login_form,
                messages=messages,
            )

    def login_checker(self, f: LoginChecker) -> LoginChecker:
        """To set login_checker as decorator:
        @simple.login_checher
        def foo(user): ...
        """
        self._login_checker = f
        return f

    def init_app(
        self,
        app: Flask,
        login_checker: LoginChecker | None = None,
        login_form: Form | None = None,
        messages: Mapping[str, Message] | None = None,
    ) -> None:
        if login_checker:
            self._login_checker = login_checker

        if login_form:
            self._login_form = login_form

        if messages and isinstance(messages, dict):
            cleaned = {k: v for k, v in messages.items() if k in self.messages}
            for key in cleaned:
                if isinstance(cleaned[key], str):
                    cleaned[key] = Message(cleaned[key])
            self.messages.update(cleaned)

        self._register(app)
        self._load_config()
        self._set_default_secret()
        self._register_views()
        self._register_extras()

    def _register(self, app: Flask) -> None:
        if not hasattr(app, "extensions"):
            app.extensions = {}

        if "simplelogin" in app.extensions:
            raise RuntimeError("Flask extension already initialized")

        app.extensions["simplelogin"] = self
        self.app = app

    def _load_config(self) -> None:
        if self.app is None:
            raise SimpleLoginNotInitializedError

        config = self.app.config.get_namespace(
            namespace="SIMPLELOGIN_", lowercase=True, trim_namespace=True
        )

        # backwards compatibility
        old_config = self.app.config.get_namespace(
            namespace="SIMPLE_LOGIN_", lowercase=True, trim_namespace=True
        )
        config.update(old_config)
        if old_config:
            msg = (
                "Settings defined as SIMPLE_LOGIN_ will be deprecated. "
                "Please, use SIMPLELOGIN_ instead."
            )
            warn(msg, FutureWarning)
            self.config.update(old_config)

        self.config.update(dict((key, value) for key, value in config.items() if value))

    def _set_default_secret(self) -> None:
        if self.app is None:
            raise SimpleLoginNotInitializedError

        if self.app.config.get("SECRET_KEY") is None:
            secret_key = str(uuid4())
            logger.warning(
                (
                    "Using random SECRET_KEY: {0}, "
                    'please set it on your app.config["SECRET_KEY"]'
                ).format(secret_key)
            )
            self.app.config["SECRET_KEY"] = secret_key

    def _register_views(self) -> None:
        if not self.app:
            raise SimpleLoginNotInitializedError(
                "Please, call `SimpleLogin.init_app(app)`"
            )

        self.blueprint = Blueprint(
            self.config["blueprint"], __name__, template_folder="templates"
        )

        self.blueprint.add_url_rule(
            self.config["login_url"],
            endpoint="login",
            view_func=self.login,
            methods=["GET", "POST"],
        )

        self.blueprint.add_url_rule(
            self.config["logout_url"],
            endpoint="logout",
            view_func=self.logout,
            methods=["GET"],
        )

        self.app.register_blueprint(self.blueprint)

    def _register_extras(self) -> None:
        if self.app is None:
            raise SimpleLoginNotInitializedError

        self.app.add_template_global(is_logged_in)
        self.app.add_template_global(get_username)

    def basic_auth(
        self, response: ResponseReturnValue | None = None
    ) -> ResponseReturnValue | bool:
        """Support basic_auth via /login or login_required(basic=True)"""
        auth = request.authorization
        if auth and self._login_checker(
            {"username": auth.username, "password": auth.password}
        ):
            session["simple_logged_in"] = True
            session["simple_basic_auth"] = True
            session["simple_username"] = auth.username
            return response or True
        else:
            headers = {"WWW-Authenticate": 'Basic realm="Login Required"'}
            return "Invalid credentials", 401, headers

    def login(self) -> ResponseReturnValue:
        if self.app is None:
            raise SimpleLoginNotInitializedError

        destiny = request.args.get(
            "next",
            default=request.form.get("next", default=self.config.get("home_url", "/")),
        )

        host_url = urlparse(request.host_url)
        redirect_url = urlparse(urljoin(request.host_url, destiny))
        if (
            host_url.netloc != redirect_url.netloc
            and redirect_url.netloc not in self.app.config.get("ALLOWED_HOSTS", [])
        ):
            return abort(400, "Invalid next url, can only redirect to the same host")

        if is_logged_in():
            self.flash("is_logged_in")
            return redirect(destiny)

        # recommended to use `login_required(basic=True)` instead this
        if request.is_json:
            resp = self.basic_auth(redirect(destiny))
            if not isinstance(resp, bool):
                return resp  # should not happen since we passed a response

        form = self._login_form()
        ret_code = 200
        if form.validate_on_submit():
            if self._login_checker(form.data):
                self.flash("login_success")
                session["simple_logged_in"] = True
                session["simple_username"] = form.data.get("username")
                return redirect(destiny)
            else:
                self.flash("login_failure")
                ret_code = 401  # <-- invalid credentials RFC7235

        return render_template("login.html", form=form, next=destiny), ret_code

    def register_on_logout_callback(self, callback: Callable) -> None:
        """Register a callback to be called on logout"""
        self.on_logout_callbacks.append(callback)

    def logout(self) -> ResponseReturnValue:
        session.clear()
        self.flash("logout")

        for callback in self.on_logout_callbacks:
            callback()

        return redirect(self.config.get("home_url", "/"))
