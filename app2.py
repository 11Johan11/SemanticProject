from flask import Flask, jsonify, request
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from flask_cors import CORS
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# OMDB API Key (Replace with your key from OMDB)
# OMDB_API_KEY = '6c33b333'

# SPARQL Endpoint for Wikidata
SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"


CSV_FILE = ".include/tmdb_5000_movies.csv"
try:
    movies_df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    raise Exception(f"CSV file '{CSV_FILE}' not found. Ensure it exists in the project directory.")


# Function to execute SPARQL queries
def execute_sparql_query(query):
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

# Fetch movie details from OMDB API
def get_movie_from_omdb(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    return response.json()

# Flask route for fetching movie recommendations
@app.route('/recommend', methods=['GET'])
def recommend_movies():
    genre = request.args.get('genre', '')
    director = request.args.get('director', '')

    # Base SPARQL query to get movies from Wikidata
    query = """
    SELECT ?movie ?movieLabel ?directorLabel ?genreLabel WHERE {
        ?movie wdt:P31 wd:Q11424.  # Instance of "film"
        OPTIONAL { ?movie wdt:P57 ?director. }
        OPTIONAL { ?movie wdt:P136 ?genre. }
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """
    
    # Add filters if genre or director are provided
    if genre:
        query = query.replace("}", f"?genre rdfs:label \"{genre}\"@en . }}")
    if director:
        query = query.replace("}", f"?director rdfs:label \"{director}\"@en . }}")

    # Execute SPARQL query to get movie data
    try:
        results = execute_sparql_query(query)
        movies = []
        for result in results["results"]["bindings"]:
            movie_name = result["movieLabel"]["value"]
            movie_data = get_movie_from_omdb(movie_name)
            movies.append(movie_data)
        return jsonify(movies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Flask route for fetching movie details by movie name
@app.route('/movie', methods=['GET'])
def movie_details():
    movie_name = request.args.get('movie_name', '')
    if not movie_name:
        return jsonify({"error": "Movie name is required"}), 400

    movie_data = get_movie_from_omdb(movie_name)
    if movie_data['Response'] == 'True':
        return jsonify(movie_data)
    else:
        return jsonify({"error": "Movie not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
