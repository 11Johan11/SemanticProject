from flask import Flask, jsonify, send_from_directory
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS
import owlrl  # For reasoning
import json
import time
from controller.search_controller import search_blueprint
from controller.recommend_controller import recommend_blueprint

from model.graph.infer import infer_graph
from flask import Flask, render_template
app = Flask(__name__, template_folder='view', static_folder='view/static', static_url_path='/static')
 

#infer_graph(["Q153723"]) inglorious bastards
#infer_graph(["Q47300912"])
#infer_graph(["Q153723","Q14786561"]) #inglorious bastards & fury
#infer_graph(["Q153723","Q166262"])#inglorious bastards & batman begins
#time.sleep(9999999)


#register Blueprints
app.register_blueprint(search_blueprint)
print(app.url_map)
app.register_blueprint(recommend_blueprint)

@app.route('/node_modules/<path:filename>')
def serve_node_modules(filename):
    return send_from_directory('node_modules', filename)

@app.route('/', methods=['GET'])
def home():
 return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)