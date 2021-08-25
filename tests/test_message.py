from flask_simplelogin import Message


def test_str():
    msg = Message("test")
    assert str(msg) == "test"
    assert msg.category == "primary"


def test_format():
    msg = Message("urgent {0}", "danger")
    assert msg.format("call") == "urgent call"
    assert msg.category == "danger"


def test_from_current_app(app):
    for key, expected in app.extensions["simplelogin"].messages.items():
        assert Message.from_current_app(key) == expected
