import pytest

from app import app as flask_app, valid_password


@pytest.fixture
def client():
    flask_app.config.update(TESTING=True)

    with flask_app.test_client() as test_client:
        yield test_client


def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_register_page_loads(client):
    response = client.get("/register")
    assert response.status_code == 200


def test_root_redirects_to_login(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_home_requires_login(client):
    response = client.get("/home", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_forum_requires_login(client):
    response = client.get("/forum", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_marketplace_requires_login(client):
    response = client.get("/marketplace", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_valid_password_accepts_strong_password():
    assert valid_password("StrongPass1!") is True


def test_valid_password_rejects_weak_passwords():
    assert valid_password("short1!") is False
    assert valid_password("NoNumber!") is False
    assert valid_password("nonumberorspecial") is False
    assert valid_password("NoSpecial1") is False