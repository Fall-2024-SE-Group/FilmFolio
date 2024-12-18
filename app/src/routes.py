"""
This module defines the routes for the Flask application.
"""

import json
import os
import requests
from dotenv import load_dotenv
from flask import jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_socketio import emit
from src import app, bcrypt, db, socket
from src.item_based import recommend_for_new_user
from src.models import Message, Movie, Review, User, WatchHistory
from src.search import Search
from werkzeug.utils import secure_filename

app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static/images/")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    """
    allowed file
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")


@app.route("/", methods={"GET"})
@app.route("/home", methods={"GET"})
def landing_page():
    """
    Renders the landing page with the user.
    """
    if current_user.is_authenticated:
        return redirect(url_for("search_page"))
    return render_template("landing_page.html")


@app.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    """
    Update the user's profile with bio, favorite genres, and profile picture.
    """
    # Get the bio and favorite genres from the form, or use current values if not provided
    bio = request.form.get("bio", current_user.bio)
    favorite_genres = request.form.get("favorite_genres", current_user.favorite_genres)

    # Handle profile picture upload
    profile_picture = request.files.get("profile_picture")

    # Only save profile picture if it is uploaded and is of an allowed type
    if profile_picture and allowed_file(profile_picture.filename):
        # Secure and save the file in the specified upload folder
        filename = secure_filename(profile_picture.filename)
        profile_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # Ensure the folder exists
        os.makedirs(os.path.dirname(profile_path), exist_ok=True)

        # Save the file
        profile_picture.save(profile_path)

        # Store relative path in the database (relative to the static/images folder)
        current_user.profile_picture = f"images/{filename}"

    # Update bio and favorite genres
    current_user.bio = bio
    current_user.favorite_genres = favorite_genres

    # Commit the changes to the database
    db.session.commit()

    # Return a success message with updated profile picture path
    return jsonify(
        {
            "success": "Profile updated successfully",
            "profile_picture": f"/static/images/{current_user.profile_picture}",
            "bio": current_user.bio,
            "favorite_genres": current_user.favorite_genres,
        }
    )


@app.route("/watch_history", methods=["GET"])
@login_required
def watch_history():
    """
    Get the user's movie watch history.
    """
    history = WatchHistory.query.filter_by(user_id=current_user.id).all()
    watched_movies = [
        {
            "movie_title": Movie.query.get(entry.movie_id).title,
            "watched_at": entry.watched_at,
        }
        for entry in history
    ]
    return jsonify(watched_movies)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Signup Page Flow
    """
    username = ""
    try:
        # If user has already logged in earlier and has an active session
        if current_user.is_authenticated:
            return redirect(url_for("search_page"))
        # If user has not logged in and a signup request is sent by the user
        if request.method == "POST":
            username = request.form["username"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            password = request.form["password"]
            hashed_password = bcrypt.generate_password_hash(password)
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=hashed_password,
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("search_page"))
        # For GET method
        return render_template("signup.html")
    # If user already exists
    # pylint: disable=broad-except
    except Exception as e:
        print(f"Error is {e}")
        message = f"Username {username} already exists!"
        return render_template("signup.html", message=message, show_message=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login Page Flow
    """
    try:
        # If user has already logged in earlier and has an active session
        if current_user.is_authenticated:
            return redirect(url_for("search_page"))
        # If user has not logged in and a login request is sent by the user
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = User.query.filter_by(username=username).first()
            # Successful Login
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("search_page"))
            # Invalid Credentials
            show_message = True
            message = "Invalid Credentials! Try again!"
            return render_template(
                "login.html", message=message, show_message=show_message
            )
        # When the login page is hit
        return render_template("login.html")
    # pylint: disable=broad-except
    except Exception as e:
        print(f"Error is {e}")
        return render_template("login.html", message=e, show_message=True)


@app.route("/logout")
def logout():
    """
    Logout Function
    """
    logout_user()
    return redirect("/")


@app.route("/profile_page", methods=["GET"])
@login_required
def profile_page():
    """
    Profile Page
    """
    reviews_objects = Review.query.filter_by(user_id=current_user.id).all()
    reviews = []
    for review in reviews_objects:
        movie_object = Movie.query.filter_by(movieId=review.movieId).first()
        obj = {
            "title": movie_object.title,
            "runtime": movie_object.runtime,
            "overview": movie_object.overview,
            "genres": movie_object.genres,
            "imdb_id": movie_object.imdb_id,
            "review_text": review.review_text,
        }
        reviews.append(obj)
    return render_template(
        "profile.html", user=current_user, reviews=reviews, search=False
    )


@app.route("/search_page", methods=["GET"])
@login_required
def search_page():
    """
    Search Page
    """
    if current_user.is_authenticated:
        return render_template("search.html", user=current_user, search=True)
    return redirect(url_for("landing_page"))


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predicts movie recommendations based on user ratings.
    """
    data = json.loads(request.data)
    data1 = data["movie_list"]
    training_data = []
    for movie in data1:
        movie_with_rating = {"title": movie, "rating": 5.0}
        if movie_with_rating not in training_data:
            training_data.append(movie_with_rating)
    data = recommend_for_new_user(training_data)
    data = data.to_json(orient="records")
    return jsonify(data)


@app.route("/search", methods=["POST"])
def search():
    """
    Handles movie search requests.
    """
    term = request.form["q"]
    finder = Search()
    filtered_dict = finder.results_top_ten(term)
    resp = jsonify(filtered_dict)
    resp.status_code = 200
    return resp


@app.route("/chat", methods=["GET"])
def chat_page():
    """
    Renders chat room page
    """
    if current_user.is_authenticated:
        return render_template("movie_chat.html", user=current_user)
    return redirect(url_for("landing_page"))


@socket.on("connections")
def show_connection(data):
    """
    Prints out if the connection to the chat page is successful
    """
    print("received message: " + data)


@socket.on("message")
def broadcast_message(data):
    """
    Distributes messages sent to the server to all clients in real-time.
    """
    print(f"Received message: {data['msg']} from {data['username']}")
    emit("message", {"username": data["username"], "msg": data["msg"]}, broadcast=True)


@app.route("/getPosterURL", methods=["GET"])
def get_poster_url():
    """
    Retrieve the poster URL for the recommended movie based on IMDb ID.
    return: JSON response containing the poster URL.
    """
    imdb_id = request.args.get("imdbID")
    poster_url = fetch_poster_url(imdb_id)
    return jsonify({"posterURL": poster_url})


def fetch_poster_url(imdb_id):
    """
    Fetch the poster URL for a movie from The Movie Database (TMDB) API.
    """
    timeout = 100
    url = (
        f"https://api.themoviedb.org/3/find/{imdb_id}?"
        f"api_key={TMDB_API_KEY}&external_source=imdb_id"
    )
    response = requests.get(url, timeout=timeout)
    data = response.json()
    # Check if movie results are present and have a poster path
    if "movie_results" in data and data["movie_results"]:
        poster_path = data["movie_results"][0].get("poster_path")
        return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    return None


@app.route("/postReview", methods=["POST"])
@login_required
def post_review():
    """
    API for the user to submit a review
    """
    # Check if the movie already exists in the database.
    # If it exists, fetch the movie ID and save the review
    # If it does not, save the movie details and save the review

    data = json.loads(request.data)
    user_object = User.query.filter_by(username=current_user.username).first()
    user_id = user_object.id
    review_text = data["review_text"]
    movie_id = data["movieId"]
    movie_object = Movie.query.filter_by(movieId=movie_id).first()
    if movie_object is None:
        # Create a new movie object
        movie = Movie(
            movieId=movie_id,
            title=data["title"],
            runtime=data["runtime"],
            overview=data["overview"],
            genres=data["genres"],
            imdb_id=data["imdb_id"],
            poster_path=data["poster_path"],
        )
        db.session.add(movie)
        db.session.commit()
    review = Review(review_text=review_text, movieId=movie_id, user_id=user_id)
    db.session.add(review)
    db.session.commit()
    return jsonify({"success": "success"})


@app.route("/movies", methods=["GET"])
@login_required
def movie_page():
    """
    Get movies and their reviews
    """
    # Get all movies
    movies_ojbects = Movie.query.all()
    movies = []

    for movie_object in movies_ojbects:
        reviews = []
        obj1 = {
            "title": movie_object.title,
            "runtime": movie_object.runtime,
            "overview": movie_object.overview,
            "genres": movie_object.genres,
            "imdb_id": movie_object.imdb_id,
        }

        # Get all reviews for each movie
        reviews_objects = Review.query.filter_by(movieId=movie_object.movieId).all()

        for review_object in reviews_objects:
            # Retrieve user for each review
            user = User.query.filter_by(id=review_object.user_id).first()

            # If user is found, get their info
            if user:
                obj2 = {
                    "username": user.username,
                    "name": f"{user.first_name} {user.last_name}",
                    "review_text": review_object.review_text,
                }
            else:
                obj2 = {
                    "username": "Anonymous",
                    "name": "Anonymous User",
                    "review_text": review_object.review_text,
                }

            reviews.append(obj2)

        obj1["reviews"] = reviews
        movies.append(obj1)

    return render_template("movie.html", movies=movies, user=current_user)


@app.route("/new_movies", methods=["GET"])
@login_required
def new_movies():
    """
    API to fetch new movies
    """
    # Replace YOUR_TMDB_API_KEY with your actual TMDb API key
    tmdb_api_key = TMDB_API_KEY
    endpoint = "https://api.themoviedb.org/3/movie/upcoming"

    # Set up parameters for the request
    params = {
        "api_key": tmdb_api_key,
        "language": "en-US",  # You can adjust the language as needed
        "page": 1,  # You may want to paginate the results if there are many
    }
    try:
        # Make the request to TMDb API
        response = requests.get(endpoint, params=params, timeout=10)
    except (
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.RequestException,
    ) as e:
        return render_template("new_movies.html", show_message=True, message=e)
    if response.status_code == 200:
        # Parse the JSON response
        movie_data = response.json().get("results", [])

        return render_template("new_movies.html", movies=movie_data, user=current_user)
    return render_template(
        "new_movies.html", show_message=True, message="Error fetching movie data"
    )


@app.route("/trends", methods=["GET"])
def trends_page():
    """
    Renders the trends page with the latest and trendy movies.
    """
    # Fetch trending movies from an API or database
    trending_movies = fetch_trending_movies()
    print(trending_movies[1])
    return render_template("trends.html", movies=trending_movies)


def fetch_trending_movies():
    """
    Fetch the trending movies from The Movie Database (TMDB) API.
    """
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_API_KEY}"
    response = requests.get(url, timeout=10)
    data = response.json()
    return data.get("results", [])


@app.route("/get_messages", methods=["GET"])
@login_required
def get_messages():
    """
    Handles loading the messages
    """
    username = current_user.username

    # Retrieve messages where the user is either sender or recipient
    received_messages = Message.query.filter_by(recipient_username=username).all()
    sent_messages = Message.query.filter_by(sender_username=username).all()

    return jsonify(
        {
            "received": [
                {
                    "id": msg.id,
                    "sender": msg.sender_username,
                    "content": msg.content,
                    "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for msg in received_messages
            ],
            "sent": [
                {
                    "id": msg.id,
                    "recipient": msg.recipient_username,
                    "content": msg.content,
                    "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for msg in sent_messages
            ],
        }
    )


@app.route("/send_message", methods=["POST"])
@login_required
def send_message():
    """
    Handles sending messages
    """
    data = request.get_json()
    sender_username = current_user.username  # Get the logged-in user's username
    recipient_username = data.get("recipient_username")
    content = data.get("content")

    if not recipient_username or not content:
        return jsonify({"error": "Recipient and content are required"}), 400

    # Check if recipient exists
    recipient = User.query.filter_by(username=recipient_username).first()
    if not recipient:
        return jsonify({"error": "Recipient not found"}), 404

    # Save the message
    message = Message(
        sender_username=sender_username,
        recipient_username=recipient_username,
        content=content,
    )
    db.session.add(message)
    db.session.commit()

    return jsonify({"message": "Message sent successfully"}), 200


@app.route("/delete_message/<int:message_id>", methods=["DELETE"])
@login_required
def delete_message(message_id):
    """
    Handles deleting the messages
    """
    message = Message.query.get(message_id)
    if not message:
        return jsonify({"error": "Message not found"}), 404

    # Only allow the sender or recipient to delete the message
    if current_user.username not in (
        message.sender_username,
        message.recipient_username,
    ):
        return (
            jsonify({"error": "You do not have permission to delete this message"}),
            403,
        )

    db.session.delete(message)
    db.session.commit()

    return jsonify({"message": "Message deleted successfully"}), 200
