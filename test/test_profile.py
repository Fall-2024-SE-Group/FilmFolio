import pytest
from app import app, db


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
        "/register",
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


def test_change_password(client):
    client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )
    client.post("/login", data={"username": "testuser", "password": "testpassword"})
    response = client.post(
        "/change_password",
        data={
            "current_password": "testpassword",
            "new_password": "newpassword",
            "confirm_password": "newpassword",
        },
    )
    assert response.status_code == 302
    assert b"Redirecting..." in response.data


def test_delete_account(client):
    client.post(
        "/register",
        data={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )
    client.post("/login", data={"username": "testuser", "password": "testpassword"})
    response = client.post("/delete_account", data={"confirm_delete": "true"})
    assert response.status_code == 302
    assert b"Redirecting..." in response.data


# the profile needs to be updated when one or more proper feilds are given


def test_update_only_bio(client):
    # User registration
    client.post(
        "/register",
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

    # Check if the status code is 200 OK
    assert response.status_code == 200

    # Check for success message in response
    assert json_data["success"] == "Profile updated successfully"

    # Check that only the bio has been updated
    assert json_data["bio"] == "Movie lover"
    assert "favorite_genres" not in json_data  # Genre shouldn't be updated
    assert "profile_picture" not in json_data  # Profile picture shouldn't be updated


def test_update_only_favorite_genres(client):
    # User registration
    client.post(
        "/register",
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

    # Check if the status code is 200 OK
    assert response.status_code == 200

    # Check for success message in response
    assert json_data["success"] == "Profile updated successfully"

    # Check that only the favorite genres have been updated
    assert json_data["favorite_genres"] == "Action, Comedy"
    assert "bio" not in json_data  # Bio shouldn't be updated
    assert "profile_picture" not in json_data  # Profile picture shouldn't be updated


def test_update_both_bio_and_favorite_genres(client):
    # User registration
    client.post(
        "/register",
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

    # Check if the status code is 200 OK
    assert response.status_code == 200

    # Check for success message in response
    assert json_data["success"] == "Profile updated successfully"

    # Check that both bio and favorite genres are updated
    assert json_data["bio"] == "Movie lover"
    assert json_data["favorite_genres"] == "Action, Comedy"
    assert "profile_picture" not in json_data  # Profile picture shouldn't be updated


def test_update_all_fields(client):
    # User registration
    client.post(
        "/register",
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

    # Check if the status code is 200 OK
    assert response.status_code == 200

    # Check for success message in response
    assert json_data["success"] == "Profile updated successfully"

    # Check that all fields (bio, favorite genres, and profile picture) are updated
    assert json_data["bio"] == "Movie lover"
    assert json_data["favorite_genres"] == "Action, Comedy"
    assert json_data["profile_picture"] == "/static/profile_picture.jpg"


def test_update_missing_bio(client):
    # User registration
    client.post(
        "/register",
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

    # Check if the status code is 200 OK
    assert response.status_code == 200

    # Check for success message in response
    assert json_data["success"] == "Profile updated successfully"

    # Check that only favorite genres have been updated, bio remains unchanged
    assert json_data["favorite_genres"] == "Action, Comedy"
    assert "bio" not in json_data  # Bio shouldn't be updated
    assert "profile_picture" not in json_data  # Profile picture shouldn't be updated


def test_update_missing_favorite_genres(client):
    # User registration
    client.post(
        "/register",
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

    # Check if the status code is 200 OK
    assert response.status_code == 200

    # Check for success message in response
    assert json_data["success"] == "Profile updated successfully"

    # Check that only bio has been updated, favorite genres remain unchanged
    assert json_data["bio"] == "Movie lover"
    assert "favorite_genres" not in json_data  # Favorite genres shouldn't be updated
    assert "profile_picture" not in json_data  # Profile picture shouldn't be updated
