from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS
from model.sparql.get_director_and_their_movies import get_director_and_their_movies

#Get the director(s) from target movie(s), and all the movies they have directed.
#Add it to the local knowledge graph to later infer relationships
def graph_for_director_movies(movie_ids,graph,NAMESPACE):

    results = get_director_and_their_movies(movie_ids)

    for result in results:
        movie_uri = URIRef(result["otherMovie"]["value"])
        movie_title = Literal(result["otherMovieName"]["value"])

        director_uri = URIRef(result["director"]["value"])
        director_name = Literal(result["directorName"]["value"])

        graph.add((movie_uri, RDF.type, NAMESPACE.Movie))
        graph.add((movie_uri, NAMESPACE.title, movie_title))

        graph.add((movie_uri, NAMESPACE.director, director_uri)) #Director type

        graph.add((director_uri, NAMESPACE.name, director_name))
        graph.add((director_uri, RDF.type, NAMESPACE.Person)) #perhaps not needed but good for future usecase

        graph.add((NAMESPACE.director, RDFS.subPropertyOf, NAMESPACE.relatedTo)) #for reasoning later

    return graph