import time
import pickle
from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLStore 



#to faster speedup loading the large ttl file (our local wikidata graph), we make sure to have it saved as a pickle 
#file, which is much faster for python to load
def save_graph_as_pickle(graph, pickle_path):
    """Save the RDF graph as a pickle file."""
    with open(pickle_path, 'wb') as f:
        pickle.dump(graph, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Graph saved as pickle at {pickle_path}")

def load_graph_from_pickle(pickle_path):
    """Load the RDF graph from a pickle file."""
    with open(pickle_path, 'rb') as f:
        graph = pickle.load(f)
    print(f"Graph loaded from pickle at {pickle_path}")
    return graph

def init_graph():
    pickle_path = "model/graph/local_graph/complete_graph.pkl"
    """
    try:
        #Try loading the graph from the pickle file
        print("Attempting to load graph from pickle...")
        graph = load_graph_from_pickle(pickle_path)
    except (FileNotFoundError, EOFError):
        #If pickle file doesn't exist or is corrupted, parse the TTL file
        print("Pickle file not found or invalid. Loading from TTL...")

        #graph.parse("model/graph/local_graph/complete_graph.ttl", format="turtle")
        print("Loaded graph from TTL")
        
        #Save the graph as a pickle for future use
        save_graph_as_pickle(graph, pickle_path)
 """
     # Initialize a persistent BerkeleyDB-backed graph
     
    endpoint_url = "http://localhost:3030/dataset/sparql"  #fuseki
    store = SPARQLStore(endpoint_url)
    store.method = 'POST'
    graph = Graph(store)
    return graph
    
