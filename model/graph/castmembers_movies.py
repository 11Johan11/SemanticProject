from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS
from model.sparql.get_cast_members_and_their_movies import get_cast_members_and_their_movies


def graph_for_castmembers_movies(movie_ids,graph,NAMESPACE):

    #Get all the castmembers from the TARGET movie(s) & Get all the movies the castmembers has participated in
    results = get_cast_members_and_their_movies(movie_ids)

    #Very important to also make sure the target movie is in the graph, forgot this before and sometimes it wasnt connected and produced no results
    for movie_id in movie_ids:
        target_movie_uri = URIRef(f"http://www.wikidata.org/entity/{movie_id}")
        graph.add((target_movie_uri, RDF.type, NAMESPACE.Movie)) 

    #Add it to the local knowledge graph to later infer relationships
    for result in results:
        movie_uri = URIRef(result["otherMovie"]["value"])
        movie_title = Literal(result["otherMovieName"]["value"])

        cast_member_uri = URIRef(result["castMember"]["value"])
        cast_member_name = Literal(result["castMemberName"]["value"])

        graph.add((movie_uri, RDF.type, NAMESPACE.Movie))
        graph.add((movie_uri, NAMESPACE.title, movie_title))

        graph.add((movie_uri, NAMESPACE.castmember, cast_member_uri)) #Castmember type
        graph.add((target_movie_uri, NAMESPACE.genre, cast_member_uri)) #Connect target movie with all castmembers

        graph.add((cast_member_uri, NAMESPACE.name, cast_member_name))
        graph.add((cast_member_uri, RDF.type, NAMESPACE.Person)) #perhaps not needed but good for future usecase

        #LATER FOR LOCAL SPARQL REASONING (INFERING)
        graph.add((NAMESPACE.castmember, RDFS.subPropertyOf, NAMESPACE.relatedTo)) #BROAD REASONING movie:relatedTo
        graph.add((NAMESPACE.castmember, RDFS.subPropertyOf, NAMESPACE.relatedPeople)) #SUB REASONING movie:relatedPeople (e.g. directors,screenwriters etc...)
        #specific would be movie:castmember

    return graph