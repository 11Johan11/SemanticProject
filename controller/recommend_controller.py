from flask import Blueprint, request, jsonify, current_app
from model.calculate_movie_points import calculate_movie_points
from combine_recommendation_data import combine_recommendation_data
from model.search.main import search,add_movie_metadata,add_person_metadata
from model.graph.infer import infer_shared_actors
import json
import time

def _map_metadata_to_recommended_movies(recommended_movies, recommended_movies_metadata):
    metadata_mapping = {meta["uri"]: meta for meta in recommended_movies_metadata}

    for movie in recommended_movies:
        movie_uri = movie["movie_uri"]
        movie["metadata"] = metadata_mapping.get(movie_uri, None)  #attach metadata or none shouldnt happen but justincase

    return recommended_movies

def extract_id_from_uri(uri):
    return uri.split("/")[-1]

recommend_blueprint = Blueprint('recommend', __name__)

@recommend_blueprint.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    movies = data.get('movies', [])

    #num movies
    movies_count = len(movies)
    print("Received Metadata:", movies)
    print("Total Movies:", movies_count)
 

    movie_ids = []
    for movie in movies:
        movie_ids.append(extract_id_from_uri(movie["uri"]))

    combined_data, original_movie_data = combine_recommendation_data(movie_ids)
    
    recommended_movies = calculate_movie_points(combined_data, original_movie_data) # !!!!!!
    recommended_movies = recommended_movies[:200] #start with 200 best


    #map them back to the searchable movies to add imdb id tags
    searchable_movies = current_app.config['SEARCHABLE_MOVIES']
    
    #extract all uris from the recommended movies
    recommended_movies_uris = []
    for data in recommended_movies:
        recommended_movies_uris.append(data["movie_uri"])
    recommended_movies_uris = set(recommended_movies_uris) #fast lookup

    #prepare a list for all recommended uris and with their imdb ids to fetch metadata for 
    fetch_movie_metadata_for_this = []
    for searchable_movie in searchable_movies:
        if searchable_movie["uri"] in recommended_movies_uris:
            fetch_movie_metadata_for_this.append(searchable_movie)


    """
    fetch_movie_metadata_for_this = []
    for movie in recommended_movies:
        fetch_movie_metadata_for_this.append({"uri": movie["movie_uri"], "imdb": None})
    """
    recommended_movies_metadata = add_movie_metadata(fetch_movie_metadata_for_this) # !!!!!!


    recommended_movies = _map_metadata_to_recommended_movies(recommended_movies, recommended_movies_metadata)
 

    #now we got everything, imdb ratings, recommmended score, everything
    #TODO IS TO DO A FINAL POLISH ON THE SCORE AND LOWER SCORES WITH BAD IMDB RATINGS
    #adjust_score_based_on_imdb_ratings()


    def adjust_score_based_on_imdb_ratings(recommended_movies):
        baseline_rating = 7.0
        low_rating_threshold = 5.0

        for movie in recommended_movies:
            metadata = movie.get("metadata", None)
            if metadata and "ratings" in metadata:
                imdb_rating = metadata["ratings"]
                imdb_rating = float(imdb_rating)
                # Calculate multiplier
                if imdb_rating < low_rating_threshold:
                    multiplier = imdb_rating/ 10.0  # Strong penalty
                else:
                    multiplier = imdb_rating / baseline_rating  # Normalization
                # Adjust points
                movie["points"] *= multiplier
            else:
                # No adjustment if no metadata or ratings
                continue

        return recommended_movies


    # Example Usage
    recommended_movies_adjusted = adjust_score_based_on_imdb_ratings(recommended_movies)
    recommended_movies_adjusted.sort(key=lambda x: x["points"], reverse=True)  #sort again
    recommended_movies_adjusted = recommended_movies_adjusted[:100] #discard the rest of the 100 potential shit movies


    return json.dumps(recommended_movies)



