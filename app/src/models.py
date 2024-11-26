from flask_login import (
    UserMixin,
)  # usermixin - Provides default implementations for user authentication
from src import db, login_manager
from datetime import datetime


@login_manager.user_loader  # Retrieves the user record from the database based on the ID
def load_user(user_id):
    """
    Function to get current user
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    User Model Table
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    reviews = db.relationship("Review", backref="user_author", lazy=True)
    # New fields for profile picture, bio, and favorite genres
    profile_picture = db.Column(db.String(200), nullable=True)  # URL or file path
    bio = db.Column(db.Text, nullable=True)
    favorite_genres = db.Column(db.String(200), nullable=True)  # Comma-separated genres

    def __repr__(self):
        return f" {self.first_name} {self.last_name}"


# pylint: disable=R0903
class Movie(db.Model):
    """
    Movie Table
    """

    movieId = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    runtime = db.Column(db.Integer, nullable=True)
    overview = db.Column(db.Text, nullable=True)
    genres = db.Column(db.String(500), nullable=False)
    imdb_id = db.Column(db.String(20), nullable=False)
    poster_path = db.Column(db.String(200), nullable=True)
    reviews = db.relationship("Review", backref="movie_author", lazy=True)

    def __repr__(self):
        return f"{self.movieId} - {self.title}"


# pylint: disable=R0903
class Review(db.Model):
    """
    Review Table
    """

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    movieId = db.Column(db.Integer, db.ForeignKey("movie.movieId"), nullable=False)

    def __repr__(self):
        return f"{self.user_id} - {self.movieId}"


class WatchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.movieId"), nullable=False)
    watched_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Watch History entry for user {self.user_id} and movie {self.movie_id}"


class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    sender_username = db.Column(db.String(80), nullable=False)
    recipient_username = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Message({self.sender_username} -> {self.recipient_username}: {self.content[:20]})"
