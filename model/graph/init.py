from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS
from model.graph.castmembers_movies import graph_for_castmembers_movies
from model.graph.director_movies import graph_for_director_movies
from model.graph.genre_movies import graph_for_genre_movies

def init_graph(movie_ids):
    g = Graph()
    MOVIE = Namespace("http://example.org/movie#")
    g.bind("movie", MOVIE)

    #BUILD THE WHOLE GRAPH
    #g = graph_for_castmembers_movies(movie_ids,g,MOVIE) 
    print("Done1")
    #g = graph_for_director_movies(movie_ids,g,MOVIE)
    print("Done2")
    g = graph_for_genre_movies(movie_ids,g,MOVIE)
    print("Done3")
    return g

