import json #used for handling HTTP request and response bodies.
import os #for fetching env variables
import requests 
import logging

from flask import render_template, flash, url_for, redirect, request,session, jsonify #jsonify - Converts Python objects into JSON format for API responses
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import emit #Sends real-time messages to clients connected via WebSocket

from dotenv import load_dotenv #Loads environment variables from a .env file into the application's environment

from src import app, db, bcrypt, socket
from src.search import Search
from src.item_based import recommend_for_new_user
from src.models import User, Movie, Review
from src.forms import RegistrationForm, LoginForm

#loading the .env file for the TMDB key
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

TMDB_BASE_URL = "https://api.themoviedb.org/3"

@app.route("/", methods={"GET"})
@app.route("/home", methods={"GET"})
def landing_page(): 
    if current_user.is_authenticated:
        return render_template("landing_page.html")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    # If user has already logged in earlier and has an active session
    if current_user.is_authenticated:
        return render_template("landing_page.html")
    
    # If user has not logged in and a signup request is sent by the user
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        try:
            user = User(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=hashed_password  
            )
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully! Welcome {user.first_name}.", "success")
            print("Registered user:", user.username, user.email)
            login_user(user)
            return redirect(url_for('search_page'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
    return render_template('signup.html', form=form, show_message=form.errors)

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        # If user has already logged in earlier and has an active session
        if current_user.is_authenticated:
            return redirect(url_for('search_page'))
        
        # Initialize the form
        form = LoginForm()

        # Check if form is being submitted via POST and is valid
        if form.validate_on_submit():
            print("Form submitted successfully")  # Debugging line
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                print("Login successful for user:", user.username)  # Debugging line
                flash(f"Login Successful. Welcome {user.first_name}!", "success")
                return redirect(url_for("search_page"))  # Redirect to search page directly
            else:
                print("Login failed: incorrect credentials")  # Debugging line
                flash("Login Unsuccessful. Please enter correct username and password.", "danger")
                return render_template("login.html", form=form)
        
        # In case of GET request, just render the login page
        return render_template("login.html", title="Login", form=form)
    except Exception as e:
        print(f"Error: {e}")
        flash('An error occurred. Please try again later.', 'danger')
        return render_template("login.html", form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('login'))

#later
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
            "title" : movie_object.title,
            "runtime" : movie_object.runtime,
            "overview" : movie_object.overview,
            "genres" : movie_object.genres,
            "imdb_id" : movie_object.imdb_id,
            "review_text" : review.review_text
        }
        reviews.append(obj)
    return render_template("profile.html", user=current_user, reviews=reviews, search=False)

@app.route("/search_page", methods=["GET"])
@login_required
def search_page(): #search page for movies
    if current_user.is_authenticated:
        return render_template("search.html", user=current_user, search=True)
    return redirect(url_for('landing_page'))

@app.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint to predict movie recommendations based on user's movie selections.
    Expects a JSON payload with a list of movie titles.
    Returns top 10 movie recommendations with their details.
    """
    try:
        # Get the JSON data from the request body
        data = json.loads(request.data)
        movie_list = data.get("movie_list", [])

        # Validate input
        if not movie_list:
            return jsonify({"error": "No movies selected"}), 400
        if not isinstance(movie_list, list):
            return jsonify({"error": "movie_list must be an array"}), 400

        # Log the incoming data
        app.logger.info(f"Incoming movie list: {movie_list}")

        # Prepare user ratings (all ratings are 5.0)
        training_data = [{"title": movie, "rating": 5.0} for movie in movie_list]
        app.logger.info(f"Prepared training data: {training_data}")

        # Get movie recommendations
        recommendations_df = recommend_for_new_user(training_data)
        
        # Validate recommendations
        if recommendations_df is None or recommendations_df.empty:
            return jsonify({"error": "No recommendations found"}), 404

        # Format recommendations for response
        recommended_movies = []
        for _, movie in recommendations_df.iterrows():
            recommended_movies.append({
                "title": movie["title"],
                "poster_path": movie["poster_path"] if "poster_path" in movie else None,
                "overview": movie["overview"] if "overview" in movie else None,
                "recommended_score": float(movie["recommended_score"]) if "recommended_score" in movie else None,
                "genres": movie["genres"] if "genres" in movie else None,
                "release_date": movie["release_date"] if "release_date" in movie else None
            })

        app.logger.info(f"Successfully generated {len(recommended_movies)} recommendations")
        app.logger.info(f"Recommendations response: {recommended_movies}")

        return recommended_movies


    except ValueError as ve:
        app.logger.error(f"Validation error in /predict route: {str(ve)}")
        return jsonify({"error": str(ve)}), 400
        
    except Exception as e:
        app.logger.error(f"Error in /predict route: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/search', methods=["POST", "GET"])
def search():
    if request.method == 'POST':
        try:
            # Check if the request has JSON content
            if not request.is_json:
                return jsonify({"error": "Content-Type must be application/json"}), 415

            # Get the query from the POST request JSON body
            data = request.get_json()
            if not data or 'query' not in data:
                return jsonify({"error": "No query provided"}), 400

            search_query = data.get('query')
            if not search_query:
                return jsonify({"error": "No query provided"}), 400

            # Search the TMDB API
            results = search_tmdb_movies(search_query)
            formatted_results = format_tmdb_results(results)
            return jsonify(formatted_results)

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # If it's a GET request, render the search page
    return render_template('search.html')
    

def search_tmdb_movies(query):
    """
    Makes a request to the TMDB API to search for movies based on the query.
    """
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&page=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()["results"]
    else:
        print(f"Error: {response.status_code}, URL: {url}")
        return []

def format_tmdb_results(results):
    """
    Formats the TMDB movie results to include necessary information.
    """
    formatted_results = []
    for movie in results:
        formatted_results.append({
            "id": movie["id"],
            "title": movie["title"],
            "overview": movie.get("overview", ""),
            "poster_path": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else "",
            "release_date": movie.get("release_date", ""),
            "rating": movie.get("vote_average", 0),
        })
    return formatted_results

@app.route("/chat", methods=["GET"])
def chat_page():
    """
        Renders chat room page
    """
    if current_user.is_authenticated:
        return render_template("movie_chat.html", user=current_user)
    return redirect(url_for('landing_page'))

@socket.on('connections')
def show_connection(data):
    """
        Prints out if the connection to the chat page is successful
    """
    print('received message: ' + data)

@socket.on('message')
def broadcast_message(data):
    """
        Distributes messages sent to the server to all clients in real time
    """
    emit('message', {'username': data['username'], 'msg': data['msg']}, broadcast=True)

logging.basicConfig(level=logging.INFO)

def get_poster_url():
    """
    Retrieve the poster URL for the recommended movie based on IMDb ID.
    return: JSON response containing the poster URL.
    """
    imdb_id = request.args.get("imdbID")
    if not imdb_id:
        logging.error("No IMDb ID provided")
        return jsonify({"error": "IMDb ID is required"}), 400

    try:
        poster_url = fetch_poster_url(imdb_id)
        if poster_url:
            return jsonify({"posterURL": poster_url})
        else:
            logging.error(f"No poster found for IMDb ID: {imdb_id}")
            return jsonify({"error": "Poster not found"}), 404
    except Exception as e:
        logging.error(f"Error fetching poster for IMDb ID {imdb_id}: {str(e)}")
        return jsonify({"error": "Failed to fetch poster"}), 500

def fetch_poster_url(imdb_id):
    """
    Fetch the poster URL for a movie from The Movie Database (TMDB) API.
    """
    timeout = 100
    url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={TMDB_API_KEY}&external_source=imdb_id"
    
    try:
        response = requests.get(url, timeout=timeout)
        
        # Check for successful response
        if response.status_code != 200:
            logging.error(f"Failed to fetch data from TMDB: {response.status_code}")
            return None
        
        data = response.json()
        
        # Check if movie results are present and have a poster path
        if "movie_results" in data and data["movie_results"]:
            poster_path = data["movie_results"][0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
            else:
                logging.warning(f"No poster_path found for IMDb ID: {imdb_id}")
        else:
            logging.warning(f"No movie results found for IMDb ID: {imdb_id}")
    
    except requests.exceptions.Timeout:
        logging.error("Request timed out while fetching poster")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error with TMDB request: {str(e)}")
    
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
    review_text = data['review_text']
    movie_id = data["movieId"]
    movie_object = Movie.query.filter_by(movieId=movie_id).first()
    if movie_object is None:
        # Create a new movie object
        movie = Movie(
            movieId = movie_id,
            title = data['title'],
            runtime = data['runtime'],
            overview = data['overview'],
            genres = data['genres'],
            imdb_id = data['imdb_id'],
            poster_path = data['poster_path']
        )
        db.session.add(movie)
        db.session.commit()
    review = Review(
        review_text = review_text,
        movieId = movie_id,
        user_id = user_id
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"success": "success"})

@app.route("/movies", methods=["GET"])
@login_required
def movie_page():
    """
    Get recent movies from TMDB and their reviews.
    """
    # Fetch recent movies from TMDB
    recent_movies = get_recent_movies_from_tmdb()

    # Movies list to store movies and their reviews
    movies = []

    for movie in recent_movies:
        reviews = []
        obj1 = {
            "title": movie["title"],
            "runtime": movie.get("runtime", "N/A"),  # Default if not available
            "overview": movie.get("overview", ""),
            "genres": movie.get("genres", ""),  # You might need to format this if genres are available
            "imdb_id": movie.get("imdb_id", ""),  # If you have IMDb ID in TMDB response
            "poster_path": movie.get("poster_path", ""),
            "release_date": movie.get("release_date", ""),
            "rating": movie.get("vote_average", 0),
        }

        # Fetch all reviews for the current movie (if any)
        reviews_objects = Review.query.filter_by(movieId=movie["id"]).all()
        user_ids = [review.user_id for review in reviews_objects]
        
        # Fetch users associated with the reviews in a single query
        users = {user.id: user for user in User.query.filter(User.id.in_(user_ids)).all()}

        for review_object in reviews_objects:
            user = users.get(review_object.user_id)
            obj2 = {
                "username": user.username if user else "Unknown User",
                "name": f"{user.first_name} {user.last_name}" if user else "Unknown",
                "review_text": review_object.review_text
            }
            reviews.append(obj2)
        
        obj1["reviews"] = reviews
        movies.append(obj1)

    return render_template("movie.html", movies=movies, user=current_user)

@app.route('/new_movies', methods=["GET"])
@login_required
def new_movies():
    """
        API to fetch new movies
    """
    tmdb_api_key = TMDB_API_KEY
    endpoint = 'https://api.themoviedb.org/3/movie/upcoming'

    # Set up parameters for the request
    params = {
        'api_key': tmdb_api_key,
        'language': 'en-US',
        'page': 1
    }
    
    try:
        # Make the request to TMDb API
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        # Log the error and display a user-friendly message
        logging.error(f"Error fetching new movies from TMDb: {str(e)}")
        return render_template('new_movies.html', show_message=True, message="Error fetching movie data")

    if response.status_code == 200:
        # Parse the JSON response
        movie_data = response.json().get('results', [])
        if not movie_data:
            logging.warning("No upcoming movies returned from TMDb API.")
            return render_template('new_movies.html', show_message=True, message="No upcoming movies found.")
        
        return render_template('new_movies.html', movies=movie_data, user=current_user)

    logging.error(f"Failed to fetch new movies. Status code: {response.status_code}")
    return render_template('new_movies.html', show_message=True, message="Error fetching movie data")

def get_movies_from_tmdb(query=''):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'language': 'en-US',
        'page': 1
    }
    response = requests.get(url, params=params)
    
    # Return movie results or empty list if no results
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        return []

@app.route('/getMovies', methods=['GET'])
def get_movies():
    query = 'romance'  # Default search query (could be dynamic based on user input)
    movies = get_movies_from_tmdb(query)
    return jsonify(movies)

def get_recent_movies_from_tmdb():
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US',
        'page': 1
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        return []

@app.route('/getRecentMovies', methods=['GET'])
def get_recent_movies():
    # Fetch the list of recent search titles from session
    recent_searches = session.get('recent_searches', [])
    
    # If there are recent searches, get their details from TMDB
    if recent_searches:
        recent_movies = []
        for search_title in recent_searches:
            url = f"{TMDB_BASE_URL}/search/movie"
            params = {
                'api_key': TMDB_API_KEY,
                'query': search_title,
                'language': 'en-US',
                'page': 1
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                results = response.json().get('results', [])
                if results:
                    recent_movies.append(results[0])  # Assuming the first result is the correct one
        return jsonify(recent_movies)
    else:
        return jsonify([])