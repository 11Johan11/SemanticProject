from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS
from model.sparql.get_genres_and_their_movies import get_genres_and_their_movies



def graph_for_genre_movies(movie_ids,graph,NAMESPACE):

    #Get all the genres from TARGET movie(s) & Get all the movies that has atleast one of the genres
    results = get_genres_and_their_movies(movie_ids) 

    #Add it to the local knowledge graph to later infer relationships
    for result in results:
        movie_uri = URIRef(result["otherMovie"]["value"])
        movie_title = Literal(result["otherMovieName"]["value"])

        genre_uri = URIRef(result["genre"]["value"])
        genre_name = Literal(result["genreName"]["value"])

        graph.add((movie_uri, RDF.type, NAMESPACE.Movie))
        graph.add((movie_uri, NAMESPACE.title, movie_title))

        graph.add((movie_uri, NAMESPACE.genre, genre_uri)) #Genre type

        graph.add((genre_uri, NAMESPACE.name, genre_name))
        graph.add((genre_uri, RDF.type, NAMESPACE.Category)) #perhaps not needed but good for future usecase

        #LATER FOR LOCAL SPARQL REASONING (INFERING)
        graph.add((NAMESPACE.genre, RDFS.subPropertyOf, NAMESPACE.relatedTo)) #BROAD REASONING movie:relatedTo
        graph.add((NAMESPACE.genre, RDFS.subPropertyOf, NAMESPACE.relatedCategory)) #SUB REASONING  movie:relatedCategory
        #The specific reasoning would just be movie:genre

    return graph