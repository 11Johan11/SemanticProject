from flask import Flask, send_from_directory
import os
from controller.search_controller import search_blueprint
from controller.recommend_controller import recommend_blueprint

from model.local_graph.init import init
from flask import Flask, render_template
app = Flask(__name__, template_folder='view', static_folder='view/static', static_url_path='/static')

#preload everything
with app.app_context():
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true": 

        graph,searchable_movies,searchable_actors,searchable_directors = init()   
           
        app.config['LOCAL_GRAPH'] = graph
        app.config['SEARCHABLE_MOVIES'] = searchable_movies
        app.config['SEARCHABLE_ACTORS'] = searchable_actors
        app.config["SEARCHABLE_DIRECTORS"] = searchable_directors 

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