from flask import url_for

from flask_simplelogin import is_logged_in


CSRF_TOKEN = "IjEwN2Q4ZjZlNWI5NjM5NjRhODk3Yzg0NzZmM2QyYjZhNzNiNDY0OWMi.YSZw7A.IUjf7OkrrCmCcg4IaV92MIrKjQ0"
CSRF_TOKEN_HASH = "107d8f6e5b963964a897c8476f3d2b6a73b4649c"


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


def test_post_with_token(client):
    with client.session_transaction() as session:
        session["csrf_token"] = CSRF_TOKEN_HASH

    client.get(url_for("simplelogin.login"))  # creates CSRF token
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


def test_is_logged_in(client):
    with client.session_transaction() as session:
        session["csrf_token"] = CSRF_TOKEN_HASH

    assert not is_logged_in()
    response = client.post(
        url_for("simplelogin.login"),
        data={
            "username": "admin",
            "password": "secret",
            "csrf_token": CSRF_TOKEN,
        },
    )
    assert response.status_code == 302
    assert is_logged_in()
