import os
import sys
from flask import render_template, request, redirect, flash, url_for, abort
import pytest

sys.path.append(os.path.join(os.getcwd(), "app"))
from src import app, db
from src.models import Vacancies, User


@pytest.fixture
def client():
    # Use an in-memory database for testing
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory database
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create database tables in the in-memory database
            yield client  # Provide the test client for tests
            db.drop_all()


@pytest.fixture
def logged_in_user(client):
    client.post("/login", data={"username": "test_user", "password": "test_password"})
    return client


def test_signup(client):
    data = {
        "username": "new_user",
        "first_name": "First",
        "last_name": "Last",
        "email": "test@example.com",
        "password": "password123",
    }
    response = client.post("/signup", data=data)
    assert response.status_code == 302  # Redirect after successful signup
    assert b"search_page" in response.headers["Location"]


def test_landing_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.data  # Update based on your landing page content


def test_update_profile(client, logged_in_user):
    data = {
        "bio": "New bio",
        "favorite_genres": "Action, Drama",
    }
    response = client.post(
        "/update_profile", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert response.json["bio"] == "New bio"
    assert "success" in response.json


def test_login(client):
    data = {"username": "test_user", "password": "test_password"}
    response = client.post("/login", data=data)
    assert response.status_code == 302
    assert b"search_page" in response.headers["Location"]


def test_logout(client, logged_in_user):
    response = client.get("/logout")
    assert response.status_code == 302
    assert b"/" in response.headers["Location"]


def test_profile_page(client, logged_in_user):
    response = client.get("/profile_page")
    assert response.status_code == 200
    assert b"Your Reviews" in response.data


def test_search_page(client, logged_in_user):
    response = client.get("/search_page")
    assert response.status_code == 200
    assert b"Search for Movies" in response.data


def test_predict(client):
    data = {"movie_list": ["Inception", "The Matrix"]}
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_search(client):
    data = {"q": "Inception"}
    response = client.post("/search", data=data)
    assert response.status_code == 200
    assert "Inception" in response.json


def test_chat_page(client, logged_in_user):
    response = client.get("/chat")
    assert response.status_code == 200
    assert b"Chat Room" in response.data


def test_trends_page(client):
    response = client.get("/trends")
    assert response.status_code == 200
    assert b"Trending Movies" in response.data


def test_send_message(client, logged_in_user):
    data = {"recipient_username": "user2", "content": "Hello!"}
    response = client.post("/send_message", json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Message sent successfully"


def test_delete_message(client, logged_in_user):
    response = client.delete("/delete_message/1")
    assert response.status_code == 200
    assert response.json["message"] == "Message deleted successfully"


def test_delete_message(client, logged_in_user):
    response = client.delete("/delete_message/1")
    assert response.status_code == 200
    assert response.json["message"] == "Message deleted successfully"


def test_new_movies(client, logged_in_user):
    response = client.get("/new_movies")
    assert response.status_code == 200
    assert b"Upcoming Movies" in response.data
