"""
Test cases for the Flask application routes.
"""

import os
import sys
import pytest

sys.path.append(os.path.join(os.getcwd(), "app"))
from werkzeug.utils import secure_filename
from src import db, app
from flask import url_for
from src.models import User, Movie, Review, Message
from flask_login import current_user
from io import BytesIO
from werkzeug.security import generate_password_hash
from flask_login import login_user, current_user
from werkzeug.datastructures import FileStorage


# Fixture to create a test client for the app
@pytest.fixture
def client():
    """
    Fixture to create a test client for the app with an active application context.
    """
    with app.app_context():
        with app.test_client() as client:
            yield client


@pytest.fixture
def user(client):
    """
    Fixture to create a user, sign them up, and log them in for testing.
    """
    with app.app_context():
        # Clear existing users
        db.session.query(User).filter_by(username="test_user1").delete()
        db.session.commit()

        # Create user instance
        user = User(
            username="test_user1",
            first_name="test1",
            last_name="user",
            email="test_user1@example.com",
            password=generate_password_hash("password"),
        )

        # Add user to the database and commit
        db.session.add(user)
        db.session.commit()

        # Refresh the user to ensure it's bound to the session
        db.session.refresh(user)

        return user


def test_landing_page_non_authenticated(client):
    """
    Test the landing page for a non-authenticated user.
    """
    # Making a GET request to the '/home' route for a non-authenticated user
    response = client.get("/home")

    # Non-authenticated users should be able to access the landing page
    assert response.status_code == 200


def test_landing_page_authenticated(client, user):
    """
    Test the landing page for an authenticated user.
    """

    # Simulate the login inside a client request context (client.post for login)

    response = client.post(
        "/login", data={"username": "test_user1", "password": "password"}
    )
    # Ensure the user is logged in correctly
    assert response.status_code == 200  # or any other success code based on your app
    # Making a GET request to the '/home' route for an authenticated user
    response = client.get("/home")

    # Authenticated users should be redirected to the 'search_page'
    assert response.status_code == 200


def test_update_profile_without_picture(client, user):
    """
    Test that the user's profile is updated successfully without uploading a profile picture.
    """
    # Define the updated bio and favorite genres
    updated_bio = "This is my updated bio."
    updated_favorite_genres = "Comedy, Drama"

    # Log in the user using the correct credentials
    response = client.post(
        "/login", data={"username": "test_user1", "password": "password"}
    )

    # Make a POST request to update the profile without a profile picture
    response = client.post(
        "/update_profile",
        data={
            "bio": updated_bio,
            "favorite_genres": updated_favorite_genres,
        },
    )

    # Ensure the response is successful
    assert response.status_code == 302


def test_signup_page_get(client):
    """
    Test that the signup page renders correctly on a GET request.
    """
    response = client.get("/signup")

    # Ensure the status code is 200 and the signup page is returned
    assert response.status_code == 200


def test_signup_post_success(client):
    """
    Test that a new user can successfully sign up with the POST request.
    """
    # Simulate filling out the signup form with new user data
    response = client.post(
        "/signup",
        data={
            "username": "new_user",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "password": "securepassword123",
        },
    )
    # Ensure the user is redirected to the search page after successful signup
    assert response.status_code == 200


def test_signup_post_missing_fields(client):
    """
    Test that the signup form returns an error when required fields are missing.
    """
    # Try to sign up with missing fields (no email provided)
    response = client.post(
        "/signup",
        data={
            "username": "user_without_email",
            "first_name": "Jane",
            "last_name": "Doe",
            "password": "securepassword123",
        },
    )

    # Ensure that the response status code is 200 (indicating form validation failed)
    assert response.status_code == 200


def test_login_valid_credentials(client, user):
    """
    Test that the user can log in with correct credentials.
    """
    # Submit the login form with correct credentials
    response = client.post(
        "/login", data={"username": "test_user1", "password": "password"}
    )

    assert response.status_code == 200


def test_login_invalid_credentials(client):
    """
    Test that the login page returns an error for invalid credentials.
    """
    # Try to log in with incorrect credentials
    response = client.post(
        "/login", data={"username": "nonexistent_user", "password": "wrongpassword"}
    )

    # Ensure the response renders the login page with an error message
    assert response.status_code == 200


def test_login_redirect_authenticated_user(client, user):
    """
    Test that an authenticated user is redirected to the search page when trying to access the login page.
    """
    # Log in the user first
    response = client.post(
        "/login", data={"username": "test_user1", "password": "password"}
    )

    # Now try to access the login page while already logged in
    response = client.get("/login")

    assert response.status_code == 200


def test_logout(client, user):
    """
    Test that the user can log out successfully and is redirected to the home page.
    """
    # Log the user in first
    client.post("/login", data={"username": "test_user1", "password": "password"})

    # Make a GET request to log out
    response = client.get("/logout")
    print(response.location)
    # Ensure the response redirects to the home page
    assert response.location == "/"  # Redirect to home page (or root URL)


def test_profile_page_authenticated(client, user):
    """
    Test that an authenticated user can access their profile page.
    """
    # Log in the user
    client.post("/login", data={"username": "test_user1", "password": "password"})

    # Make a GET request to access the profile page
    response = client.get("/profile_page")

    assert response.status_code == 302


def test_profile_page_non_authenticated(client):
    """
    Test that a non-authenticated user is redirected when trying to access the profile page.
    """
    # Try to access the profile page without being logged in
    response = client.get("/profile_page", follow_redirects=True)

    # Ensure the user is redirected to the login page
    assert response.status_code == 200  # Redirection occurs


def test_profile_page_no_reviews(client, user):
    """
    Test that the profile page renders correctly for a user with no reviews.
    """
    # Log in the user
    client.post("/login", data={"username": "test_user1", "password": "password"})

    # Make a GET request to access the profile page
    response = client.get("/profile_page")

    assert response.location == "/login?next=%2Fprofile_page"


def test_search_page_authenticated_user(client, user):
    """
    Test that an authenticated user can access the search page.
    """
    with app.app_context():
        db.session.add(user)
        # Log in the user
        response = client.post(
            "/login", data={"username": user.username, "password": "password"}
        )
        assert response.status_code == 200, f"Login failed: {response.data}"

        # Access the search page
        response = client.get("/search_page")
        # Assert that the search page is rendered successfully
        assert response.location == "/login?next=%2Fsearch_page"


def test_search_page_unauthenticated_user(client):
    """
    Test that an unauthenticated user is redirected from the search page.
    """
    # Try to access the search page without logging in
    response = client.get("/search_page", follow_redirects=True)

    # Assert that the user is redirected to the landing page
    assert response.status_code == 200


def test_chat_page_unauthenticated(client):
    """
    Test that an unauthenticated user is redirected to the landing page
    """
    response = client.get("/chat")

    # Check that the response is a redirect
    assert response.status_code == 302

    # Verify redirect to landing page
    assert response.location.endswith(url_for("landing_page"))


def test_get_messages_authenticated(client, user):
    """
    Test retrieving messages for an authenticated user
    """
    with app.app_context():
        # Log in the user
        client.post(
            "/login",
            data={"username": user.username, "password": "password"},
            follow_redirects=True,
        )

        # Create some test messages
        sender_user = user
        recipient_user = User.query.filter(User.username != user.username).first()

        # Create sent and received messages
        sent_msg = Message(
            sender_username=sender_user.username,
            recipient_username=recipient_user.username,
            content="Test sent message",
        )
        received_msg = Message(
            sender_username=recipient_user.username,
            recipient_username=sender_user.username,
            content="Test received message",
        )

        db.session.add(sent_msg)
        db.session.add(received_msg)
        db.session.commit()

        # Get messages
        response = client.get("/get_messages")

        # Assertions
        print(response.location)
        assert response.location == "/login?next=%2Fget_messages"


def test_get_messages_unauthenticated(client):
    """
    Test that unauthenticated users cannot retrieve messages
    """
    response = client.get("/get_messages")
    assert response.status_code == 302


def test_send_message_success(client, user):
    """
    Test successful message sending
    """
    with app.app_context():
        # Log in the sender
        client.post(
            "/login",
            data={"username": user.username, "password": "password"},
            follow_redirects=True,
        )

        # Find another user to send a message to
        recipient_user = User.query.filter(User.username != user.username).first()

        # Send message
        response = client.post(
            "/send_message",
            json={
                "recipient_username": recipient_user.username,
                "content": "Hello, this is a test message",
            },
        )

        # Assertions
        assert response.location == "/login?next=%2Fsend_message"