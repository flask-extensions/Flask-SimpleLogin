from unittest.mock import call

from flask import session, url_for
from itsdangerous import URLSafeTimedSerializer

from flask_simplelogin import is_logged_in


def test_get_login(client):
    response = client.get(url_for("simplelogin.login"))
    assert response.status_code == 200
    assert '<form action="/login/' in str(response.data)


def test_post_requires_token(client):
    response = client.post(
        url_for("simplelogin.login"), data={"username": "admin", "password": "secret"}
    )
    assert response.status_code == 200
    assert "csrf_token The CSRF token is missing" in str(response.data)


def test_post_with_token(app, client):
    response = client.post(
        url_for("simplelogin.login"),
        data={
            "username": "admin",
            "password": "secret",
            "csrf_token": "not a CSRF token",
        },
    )
    assert response.status_code == 200
    assert "csrf_token The CSRF token is missing" not in str(response.data)


def test_negative_redirect_to_external_url(client):
    response = client.get(
        url_for("simplelogin.login", next="https://malicioussite.com/pwowned"),
        follow_redirects=True,
    )
    assert response.status_code == 400
    assert "Invalid next url" in str(response.data)


def test_positive_redirect_to_allowed_host(app):
    app.config["ALLOWED_HOSTS"] = ["myothersite.com"]
    with app.test_client() as client:
        response = client.get(
            url_for("simplelogin.login", next="https://myothersite.com/page"),
            follow_redirects=True,
        )
        assert response.status_code == 200


def test_is_logged_in(app, client):
    def generate_csrf_token_form_value(app):
        """Based on how Flask-WTF generates it on the fly:
        https://github.com/wtforms/flask-wtf/blob/main/src/flask_wtf/csrf.py#L54-L63
        """
        return URLSafeTimedSerializer(
            app.config["SECRET_KEY"], salt="wtf-csrf-token"
        ).dumps(session["csrf_token"])

    client.get(url_for("simplelogin.login"))
    assert not is_logged_in()
    response = client.post(
        url_for("simplelogin.login"),
        data={
            "username": "admin",
            "password": "secret",
            "csrf_token": generate_csrf_token_form_value(app),
        },
    )
    assert response.status_code == 302
    assert is_logged_in()
