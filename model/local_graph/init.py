import time
import pickle
from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLStore 
import json
import base64


def get_fuseki_query_access():
    # Your Virtuoso SPARQL endpoint
    endpoint_url = "http://localhost:8890/sparql"

    # Create the SPARQL store
    store = SPARQLStore(endpoint_url)
    store.method = 'POST'

    # Encode Basic Authentication credentials
    username = "dba"
    password = "dba"
    credentials = f"{username}:{password}"
    base64_credentials = base64.b64encode(credentials.encode()).decode()

    # Add Authorization header
    store.headers = {
        "Authorization": f"Basic {base64_credentials}"
    }

    # Create an rdflib graph linked to the SPARQL store
    graph = Graph(store)

    return graph

"""
def get_fuseki_query_access():
     
    #endpoint_url = "http://localhost:3030/dataset/sparql"  #fuseki
    endpoint_url = "http://localhost:8890/sparql"
    store = SPARQLStore(endpoint_url)
    store.method = 'GET'
    graph = Graph(store) 
    return graph
"""    

def get_searchable_entities(g):
    def load_movies(g):
        movies = None
        try:
            print("Trying to preload movie dump from json file....")
            with open("model/search/search_movie_dump.json", "r", encoding="utf-8") as f:
                movies = json.load(f)
                
        #query our local graph and load & dump
        except (FileNotFoundError, EOFError):
            print("Movie dump not found, Querying local graph for a new dump...")
            local_query = """
                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

                SELECT DISTINCT ?movie ?movieName ?imdb ?publicationDate WHERE {
                    ?movie rdf:type wd:Q11424.       #instance of a film (movie) TODO: fix so we have like wikidata  wdt:P31
                    ?movie wdt:P345 ?imdb.          #must have an IMDb ID
                    ?movie rdfs:label ?movieName.
                    OPTIONAL { ?movie wdt:P577 ?publicationDate. }  # optional publication date                 
                }
            """
            movies = []
            for row in g.query(local_query):
                movies.append({
                    "uri": str(row.movie),
                    "name": str(row.movieName),
                    "imdb": str(row.imdb),
                    "publicationDate": str(row.publicationDate) if row.publicationDate else ""  # Handle missing publicationDate
                })
            with open("model/search/search_movie_dump.json", "w", encoding="utf-8") as f:
                json.dump(movies, f, indent=4, ensure_ascii=False)

        print("Movies loaded")
        return movies

    def load_actors(g):
        actors = None
        try:
            print("Trying to preload actor dump from json file....")
            with open("model/search/search_actor_dump.json", "r", encoding="utf-8") as f:
                actors = json.load(f)
                
        #query our local graph and load & dump
        except (FileNotFoundError, EOFError):
            print("Actor dump not found, Querying local graph for a new dump...")
            local_query = """

                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

                SELECT DISTINCT ?actor ?actorName WHERE {
                    ?movie wdt:P161 ?actor.       
                    ?actor rdfs:label ?actorName.        
                }
            """
            actors = []
            for row in g.query(local_query):
                actors.append({"uri": str(row.actor), "name": str(row.actorName)});

            with open("model/search/search_actor_dump.json", "w", encoding="utf-8") as f:
                json.dump(actors, f, indent=4, ensure_ascii=False)

        print("Actors loaded")
        return actors

    def load_directors(g):
        directors = None
        try:
            print("Trying to preload directors dump from json file....")
            with open("model/search/search_director_dump.json", "r", encoding="utf-8") as f:
                directors = json.load(f)
                
        #query our local graph and load & dump
        except (FileNotFoundError, EOFError):
            print("Director dump not found, Querying local graph for a new dump...")
            local_query = """
            
                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

                SELECT DISTINCT ?director ?directorName WHERE {
                    ?movie wdt:P57 ?director.       
                    ?director rdfs:label ?directorName.        
                }
            """
            directors = []
            for row in g.query(local_query):
                directors.append({"uri": str(row.director), "name": str(row.directorName)});

            with open("model/search/search_director_dump.json", "w", encoding="utf-8") as f:
                json.dump(directors, f, indent=4, ensure_ascii=False)

        print("Directors loaded")
        return directors

    searchable_movies = load_movies(g)
    searchable_actors = load_actors(g)
    searchable_directors = load_directors(g)

    return searchable_movies,searchable_actors,searchable_directors


def init():
    g = get_fuseki_query_access()
    searchable_movies,searchable_actors,searchable_directors = get_searchable_entities(g)

    return g,searchable_movies,searchable_actors,searchable_directors
