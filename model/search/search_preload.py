import time
from SPARQLWrapper import SPARQLWrapper, JSON
import json

#Fetch ALL Movie uris, Movie Titles, IMDB ids 
#Dump it into a JSON file for later use
#(used to optimize search and connect with TMDBP Api for movie posters)  (connecting made with wikidata id)

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
            SELECT DISTINCT ?movie ?movieName ?imdb WHERE {
                ?movie rdf:type wd:Q11424.       #instance of a film (movie) TODO: fix so we have like wikidata  wdt:P31
                ?movie wdt:P345 ?imdb.          #must have an IMDb ID
                ?movie rdfs:label ?movieName.
            }
        """
        movies = []
        for row in g.query(local_query):
            movies.append({"uri": str(row.movie), "name": str(row.movieName), "imdb": str(row.imdb)});

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