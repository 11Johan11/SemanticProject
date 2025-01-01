from flask import Blueprint, request, jsonify
from model.graph.infer import infer_graph

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

    print(movie_ids)
    infer_graph(movie_ids)

    return jsonify("hello")
