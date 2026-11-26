import pytest
from app import create_app
from app.extensions import db
from app.posts.models import User


@pytest.fixture()
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def register(client, username="student", email="student@example.com", password="secret123"):
    return client.post("/users/register", data={
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": password,
    }, follow_redirects=True)


def login(client, email="student@example.com", password="secret123"):
    return client.post("/users/login", data={
        "email": email,
        "password": password,
    }, follow_redirects=True)


def test_register_page_loads(client):
    response = client.get("/users/register")
    assert response.status_code == 200
    assert "Реєстрація".encode() in response.data


def test_login_page_loads(client):
    response = client.get("/users/login")
    assert response.status_code == 200
    assert "Вхід до профілю".encode() in response.data


def test_registration_saves_hashed_password(app, client):
    response = register(client)
    assert response.status_code == 200
    assert "Реєстрація успішна".encode() in response.data
    with app.app_context():
        user = db.session.query(User).filter_by(email="student@example.com").first()
        assert user is not None
        assert user.password != "secret123"
        assert user.check_password("secret123") is True
        assert user.check_password("wrong-password") is False


def test_duplicate_username_or_email_is_rejected(client):
    register(client)
    # Registration automatically authenticates the user; log out before another attempt.
    client.post("/users/logout")
    response = register(client, username="student", email="another@example.com")
    assert "ім’я користувача вже зайняте".encode() in response.data


def test_login_with_correct_password(client):
    register(client)
    client.post("/users/logout")
    response = login(client)
    assert response.status_code == 200
    assert "Профіль".encode() in response.data or "student".encode() in response.data


def test_login_with_wrong_password_is_rejected(client):
    register(client)
    client.post("/users/logout")
    response = login(client, password="incorrect")
    assert "Неправильна електронна адреса або пароль".encode() in response.data


def test_account_and_user_list_require_login(client):
    account_response = client.get("/users/account")
    users_response = client.get("/users/all")
    assert account_response.status_code == 302
    assert "/users/login" in account_response.headers["Location"]
    assert users_response.status_code == 302
    assert "/users/login" in users_response.headers["Location"]


def test_logout_ends_session(client):
    register(client)
    client.post("/users/logout")
    response = client.get("/users/account")
    assert response.status_code == 302
    assert "/users/login" in response.headers["Location"]


def test_authorized_user_can_open_user_list(client):
    register(client)
    response = client.get("/users/all")
    assert response.status_code == 200
    assert "student".encode() in response.data
    assert "Кількість користувачів".encode() in response.data
