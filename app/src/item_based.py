import os
import pandas as pd
import requests
from dotenv import load_dotenv

# Loading the .env file for the TMDB key
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise ValueError("TMDB API key is missing in the environment variables.")

def recommend_for_new_user(user_ratings):
    """
    Generates a list of recommended movie titles for a new user based on their ratings.
    
    Args:
        user_ratings (list): List of dictionaries containing movie titles and ratings
            [{'title': 'Movie Name', 'rating': 5.0}, ...]
    
    Returns:
        pd.DataFrame: Top 10 recommended movies with their details
    """
    # Fetch movie data from TMDB
    movies = fetch_movies_from_tmdb()
    
    # Convert user ratings into a DataFrame
    user_df = pd.DataFrame(user_ratings)
    print("User ratings DataFrame:", user_df)

    # Match user-rated movies with our movie database
    user_movie_matches = movies[movies["title"].isin(user_df["title"])].copy()
    if user_movie_matches.empty:
        print("Warning: No exact matches found in the database")
        return movies.head(10)  # Return top-rated movies as fallback
    
    # Merge ratings with matched movies
    user_ratings_df = pd.merge(user_movie_matches, user_df, on="title", how="inner", suffixes=('_movie', '_user'))
    print("Merged user ratings:", user_ratings_df)

    # Process genres for all movies
    genres_list = []
    for movie_genres in movies['genres'].str.split('|'):
        if isinstance(movie_genres, list):
            genres_list.extend(movie_genres)
    unique_genres = list(set(filter(None, genres_list)))

    # Create genre matrix for all movies
    genre_matrix = pd.DataFrame(0, index=movies.index, columns=unique_genres)
    
    # Fill in genre matrix
    for idx, row in movies.iterrows():
        if pd.notna(row['genres']):
            movie_genres = row['genres'].split('|')
            for genre in movie_genres:
                if genre in unique_genres:
                    genre_matrix.loc[idx, genre] = 1

    # Calculate user profile
    user_profile = pd.Series(0, index=unique_genres)
    for _, row in user_ratings_df.iterrows():
        movie_idx = movies[movies['title'] == row['title']].index[0]
        movie_genres = genre_matrix.loc[movie_idx]
        # Use the user's rating from the rating column
        user_profile += movie_genres * row['rating_user']
    user_profile = pd.to_numeric(user_profile, downcast="float")

    # Normalize user profile
    if user_profile.sum() > 0:
        user_profile = user_profile / user_profile.sum()

    # Calculate similarity scores
    similarity_scores = pd.Series(0, index=movies.index, dtype="float64")
    for idx in movies.index:
        movie_genres = genre_matrix.loc[idx]
        similarity_scores[idx] = (movie_genres * user_profile).sum()

    # Add scores to movies DataFrame
    recommendations = movies.copy()
    recommendations['recommended_score'] = similarity_scores

    # Sort by recommendation score and filter out already rated movies
    recommendations = recommendations[~recommendations['title'].isin(user_df['title'])]
    recommendations = recommendations.sort_values('recommended_score', ascending=False)

    # If we don't have enough recommendations, pad with top-rated movies
    if len(recommendations) < 10:
        remaining_count = 10 - len(recommendations)
        top_rated = movies[~movies['title'].isin(recommendations['title'])].nlargest(remaining_count, 'rating')
        recommendations = pd.concat([recommendations, top_rated])

    # Ensure we have all required columns in the output
    recommendations = recommendations[['title', 'genres', 'overview', 'poster_path', 'release_date', 'rating', 'recommended_score']]
    
    return recommendations.head(10)

def fetch_movies_from_tmdb():
    """
    Fetch movies from TMDB API and format them for recommendation.
    """
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&page=1"
    response = requests.get(url)
    movies = []

    if response.status_code == 200:
        results = response.json()["results"]
        
        # Fetch genre mapping once
        genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}"
        genre_response = requests.get(genre_url)
        if genre_response.status_code != 200:
            raise Exception("Failed to fetch genre mapping from TMDB")
        
        genre_map = {g['id']: g['name'] for g in genre_response.json()['genres']}
        
        for movie in results:
            # Map genre IDs to names
            genre_names = [genre_map.get(gid, '') for gid in movie.get('genre_ids', [])]
            genre_names = [name for name in genre_names if name]  # Remove empty strings
            
            movies.append({
                "movieId": movie["id"],
                "title": movie["title"],
                "genres": "|".join(genre_names),
                "overview": movie.get("overview", ""),
                "poster_path": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else "",
                "release_date": movie.get("release_date", ""),
                "rating": movie.get("vote_average", 0),
            })
    else:
        raise Exception(f"Failed to fetch movies from TMDB. Status code: {response.status_code}")

    return pd.DataFrame(movies)