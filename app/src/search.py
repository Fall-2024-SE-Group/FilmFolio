import os
import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TMDB_API_KEY = 'your_tmdb_api_key'  # Replace with your actual TMDB API key
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

class Search:
    """
    Search feature for landing page
    """

    def __init__(self):
        pass

    def search_tmdb(self, query):
        """
        Function to fetch movie data from TMDB
        """
        url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            'api_key': TMDB_API_KEY,
            'query': query,
            'language': 'en-US',
            'page': 1,
            'include_adult': 'false'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()['results']
        else:
            return []

    def starts_with(self, word, movie_data):
        """
        Function to check movie prefix from TMDB data
        """
        n = len(word)
        res = []
        word = word.lower()
        for movie in movie_data:
            title = movie['title'].lower()
            if title[:n] == word:
                res.append(movie)
        return res

    def anywhere(self, word, visited_words, movie_data):
        """
        Function to check visited words from TMDB data
        """
        res = []
        word = word.lower()
        for movie in movie_data:
            if movie['title'] not in visited_words:
                title = movie['title'].lower()
                if word in title:
                    res.append(movie)
        return res

    def results(self, word):
        """
        Function to serve the result render
        """
        movie_data = self.search_tmdb(word)
        starts_with = self.starts_with(word, movie_data)
        visited_words = set([movie['title'] for movie in starts_with])
        anywhere = self.anywhere(word, visited_words, movie_data)
        starts_with.extend(anywhere)
        return starts_with

    def results_top_ten(self, word):
        """
        Function to get top 10 results
        """
        return self.results(word)[:10]

#if __name__ == "__main__":
#    app.run()