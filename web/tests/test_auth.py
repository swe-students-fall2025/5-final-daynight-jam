import pytest
from unittest.mock import patch
from web.app.auth import create_user, find_user_by_username, User

def test_create_user_success():
    """Creating a new user should return True and store the user."""
    ok = create_user("bob", "abc123")
    assert ok is True

    user = find_user_by_username("bob")
    assert user is not None
    assert user["username"] == "bob"
    assert "password" in user


def test_create_user_duplicate():
    """Creating a duplicate user should return False."""
    create_user("jen", "abc123")
    ok = create_user("jen", "abc456")
    assert ok is False


def test_find_user_by_username_not_found():
    assert find_user_by_username("ghost") is None


def test_register_missing_fields(client):
    response = client.post("/auth/register", data={"username": "", "password": ""})
    assert b"Username and password are required" in response.data


def test_register_success(client):
    response = client.post("/auth/register", data={
        "username": "newuser",
        "password": "123"
    }, follow_redirects=True)

    assert b"Registration successful" in response.data


def test_register_duplicate(client):
    client.post("/auth/register", data={"username": "sam", "password": "pw"})
    response = client.post("/auth/register", data={
        "username": "sam",
        "password": "pw"
    })

    assert b"That username is already taken" in response.data


def test_login_missing_fields(client):
    response = client.post("/auth/login", data={"username": "", "password": ""})
    assert b"Username and password are required" in response.data

def test_login_invalid_user(client):
    response = client.post("/auth/login", data={"username": "nobody", "password": "pw"})
    assert b"Invalid username or password" in response.data


def test_login_wrong_password(client):
    client.post("/auth/register", data={"username": "alice", "password": "pw1"})
    # Wrong password
    response = client.post("/auth/login", data={"username": "alice", "password": "wrong"})
    assert b"Invalid username or password" in response.data


def test_login_success(client):
    client.post("/auth/register", data={"username": "mark", "password": "pw"})

    response = client.post("/auth/login", data={"username": "mark", "password": "pw"},
                           follow_redirects=True)

    # Redirects to pages.home
    assert response.status_code == 200


def test_logout_requires_login(client):
    response = client.get("/auth/logout", follow_redirects=True)
    # Should redirect to login
    assert b"Login" in response.data or b"login" in response.data


def test_logout_success(client):
    # Register + login
    client.post("/auth/register", data={"username": "test", "password": "pw"})
    client.post("/auth/login", data={"username": "test", "password": "pw"})

    response = client.get("/auth/logout", follow_redirects=True)
    assert b"logged out" in response.data.lower()


def test_me_authenticated(client):
    client.post("/auth/register", data={"username": "john", "password": "pw"})
    client.post("/auth/login", data={"username": "john", "password": "pw"})

    response = client.get("/auth/me")
    assert response.json == {"username": "john"}


def test_me_unauthenticated(client):
    response = client.get("/auth/me")
    assert response.json == {"username": None}
