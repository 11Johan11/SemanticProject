from flask import Flask, send_from_directory
import os
from controller.search_controller import search_blueprint
from controller.recommend_controller import recommend_blueprint

from model.graph.init import init_graph
from model.search.search_preload import load_movies, load_actors, load_directors
from flask import Flask, render_template

app = Flask(__name__, template_folder='view', static_folder='view/static', static_url_path='/static')

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