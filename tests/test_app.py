from flask import url_for, session

# from flask_simplelogin import is_logged_in


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
    session.clear()
    session["csrf_token"] = "123456"
    response = client.post(
        url_for("simplelogin.login"),
        data={"username": "admin", "password": "secret", "csrf_token": "123456"},
    )
    assert response.status_code == 200
    assert "csrf_token The CSRF token is missing" not in str(response.data)
    # token is still invalid :(


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


# def test_is_logged_in(client):
#     session.clear()
#     session['csrf_token'] = '123456'
#     response = client.post(
#         url_for('simplelogin.login'),
#         data={
#             'username': 'admin',
#             'password': 'secret',
#             'csrf_token': '123456'
#         }
#     )
#     assert response.status_code == 200
#     print(response.data)
#     # assert is_logged_in() is True
