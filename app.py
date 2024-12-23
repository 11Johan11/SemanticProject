from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the movie dataset
CSV_FILE = "./include/tmdb_5000_movies.csv"
movies_df = pd.read_csv(CSV_FILE)
print(movies_df)
# SPARQL Endpoint for Wikidata
SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

# Function to execute SPARQL queries
def execute_sparql_query(query):
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

# Route for the homepage
@app.route('/')
def index():
    # return print("Hello Words")
    return render_template("index.html")

# Route to fetch recommendations
@app.route('/recommendations', methods=['GET','POST'])
def recommendations():
    preferences = request.form
    id = preferences.get('id', '').lower()
    print(id)
    # genre = preferences.get('genre', '').lower()
    # director = preferences.get('director', '').lower()
    # actor = preferences.get('actor', '').lower()

    # Filter movies based on CSV
    filtered_df = movies_df
    if id:
        filtered_df = filtered_df[filtered_df['id'].str.lower().str.contains(id, na=False)]
    # if genre:
    #     filtered_df = filtered_df[filtered_df['genres'].str.lower().str.contains(genre, na=False)]
    # if director:
    #     filtered_df = filtered_df[filtered_df['director'].str.lower().str.contains(director, na=False)]

    # Limit to 10 movies
    movies = filtered_df.head(10)
    print(movies)
    # Fetch actor's movies using SPARQL
    sparql_results = []
    if id:
        query=f"""
        SELECT * WHERE {{
            ?movie wdt:P31 wd:Q11424.  # Instance of "film"
            ?movie wdt:P161 ?id.   # Starring actor
            ?id rdfs:label "{id}"@en.
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        """
        sparql_results = execute_sparql_query(query)
    print("==============================================")
    print(sparql_results)
    # if actor:
    #     query = f"""
    #     SELECT * WHERE {{
    #         ?movie wdt:P31 wd:Q11424.  # Instance of "film"
    #         ?movie wdt:P161 ?actor.   # Starring actor
    #         ?actor rdfs:label "{actor}"@en.
    #         SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    #     }}
    #     LIMIT 5
    #     """
    #     sparql_results = execute_sparql_query(query)
    return render_template('recommendations.html', id=id, sparql_results=sparql_results)


# Error handling
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error_message="Page not found!"), 404

if __name__ == '__main__':
    app.run(debug=True)
