import pytest
import os
import sys
import pytest

sys.path.append(os.path.join(os.getcwd(), "app"))

from src import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()


def test_update_profile(client):
    client.post(
        "/signup",
        data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )
    client.post("/login", data={"username": "testuser", "password": "testpassword"})
    response = client.post(
        "/update_profile",
        data={"email": "newemail@example.com", "bio": "I love movies!"},
    )
    assert response.status_code == 302
    assert b"Redirecting..." in response.data


# the profile needs to be updated when one or more proper feilds are given


def test_update_only_bio(client):
    # User registration
    client.post(
        "/signup",
        data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )

    # User login
    client.post("/login", data={"username": "testuser", "password": "testpassword"})

    # Simulate profile update with only bio
    response = client.post("/update_profile", data={"bio": "Movie lover"})

    json_data = response.get_json()

    assert response.status_code == 302


def test_update_only_favorite_genres(client):
    # User registration
    client.post(
        "/signup",
        data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )

    # User login
    client.post("/login", data={"username": "testuser", "password": "testpassword"})

    # Simulate profile update with only favorite genres
    response = client.post(
        "/update_profile", data={"favorite_genres": "Action, Comedy"}
    )

    json_data = response.get_json()

    assert response.status_code == 302


def test_update_both_bio_and_favorite_genres(client):
    # User registration
    client.post(
        "/signup",
        data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )

    # User login
    client.post("/login", data={"username": "testuser", "password": "testpassword"})

    # Simulate profile update with both bio and favorite genres
    response = client.post(
        "/update_profile",
        data={"bio": "Movie lover", "favorite_genres": "Action, Comedy"},
    )

    json_data = response.get_json()

    assert response.status_code == 302


def test_update_all_fields(client):
    # User registration
    client.post(
        "/signup",
        data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )

    # User login
    client.post("/login", data={"username": "testuser", "password": "testpassword"})

    # Simulate profile update with bio, favorite genres, and profile picture
    response = client.post(
        "/update_profile",
        data={
            "bio": "Movie lover",
            "favorite_genres": "Action, Comedy",
            "profile_picture": "profile_picture.jpg",
        },
    )

    json_data = response.get_json()

    assert response.status_code == 302


def test_update_missing_bio(client):
    # User registration
    client.post(
        "/signup",
        data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )

    # User login
    client.post("/login", data={"username": "testuser", "password": "testpassword"})

    # Simulate profile update with missing bio
    response = client.post(
        "/update_profile", data={"favorite_genres": "Action, Comedy"}
    )

    json_data = response.get_json()

    assert response.status_code == 302


def test_update_missing_favorite_genres(client):
    # User registration
    client.post(
        "/signup",
        data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )

    # User login
    client.post("/login", data={"username": "testuser", "password": "testpassword"})

    # Simulate profile update with missing favorite genres
    response = client.post("/update_profile", data={"bio": "Movie lover"})

    json_data = response.get_json()

    assert response.status_code == 302
