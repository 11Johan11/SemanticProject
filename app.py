from flask import Flask, jsonify, send_from_directory
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS
import owlrl  # For reasoning
import json
import time
from flask import g
import os
from controller.search_controller import search_blueprint
from controller.recommend_controller import recommend_blueprint

from model.graph.infer import infer_shared_actors, infer_shared_genres, fetch_and_map_actor_metadata, filter_actor_popularity, fetch_and_map_director_metadata, infer_shared_directors, fetch_publicationdate
from model.graph.init import init_graph
from model.search.search_preload import load_movies, load_actors, load_directors
from combine_recommendation_data import combine_recommendation_data

#maga = filter_actor_popularity(fetch_and_map_actor_metadata(infer_shared_actors(["Q153723","Q14786561"])), threshold=30)
#with open("movies_that_shared_actors.json", "w", encoding="utf-8") as file:
#    json.dump(maga, file, ensure_ascii=False, indent=2)
#time.sleep(99999)

""""
maga = fetch_and_map_director_metadata(infer_shared_directors(["Q153723","Q14786561"]))
with open("movies_that_shared_directors.json", "w", encoding="utf-8") as file:
    json.dump(maga, file, ensure_ascii=False, indent=2)
time.sleep(99999)
"""


combine_recommendation_data(["Q153723","Q14786561"])
#print(fetch_publicationdate(["Q153723","Q14786561"]))
time.sleep(99999)

from flask import Flask, render_template


app = Flask(__name__, template_folder='view', static_folder='view/static', static_url_path='/static')
 

#infer_shared_genres(["Q153723"])
#time.sleep(99999)


#infer_shared_actors(["Q153723"]) #inglorious bastards
#infer_shared_actors(["Q217189"])
#infer_shared_actors(["Q153723","Q14786561"]) #inglorious bastards & fury
#infer_shared_actors(["Q153723","Q166262"])#inglorious bastards & batman begins

#infer_shared_genres(["Q676513"])

#infer_shared_actors(["Q153723","Q166262"])
#time.sleep(9999999)


#preload everything
with app.app_context():
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":

        #preload our graph
        graph = init_graph()
        app.config['LOCAL_GRAPH'] = graph

        #preload the searchable movies
        movies = load_movies(graph)
        app.config['SEARCHABLE_MOVIES'] = movies

        #preload the searchable actors
        actors = load_actors(graph)
        app.config['SEARCHABLE_ACTORS'] = actors

        directors = load_directors(graph)
        app.config["SEARCHABLE_DIRECTORS"] = directors        

#register Blueprints
app.register_blueprint(search_blueprint)
#print(app.url_map)
app.register_blueprint(recommend_blueprint)

@app.route('/node_modules/<path:filename>')
def serve_node_modules(filename):
    return send_from_directory('node_modules', filename)

@app.route('/', methods=['GET'])
def home():
 return render_template('index.html')

if __name__ == '__main__':

    app.run(debug=True)