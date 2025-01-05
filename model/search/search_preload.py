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


    return movies