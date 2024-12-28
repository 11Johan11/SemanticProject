from model.graph.init import init_graph 
import owlrl
import time

def infer_graph(movie_ids): #EXAMPLE EARLY STAGES
    g = init_graph(movie_ids) 

    #apply reasoning
    owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)

    #query the graph for inferred relationships

    target_movie_count = len(movie_ids)

    movie_filter = " ".join(f"<http://www.wikidata.org/entity/{movie}>" for movie in movie_ids) 
    print(movie_filter)
    #Count shared cast members for specific movie(s)
    query = """
    SELECT DISTINCT ?sharedCastMember ?otherMovie (COUNT(DISTINCT ?sharedCastMember) AS ?sharedCount)
    WHERE {{
        VALUES ?targetMovie {{ {movie_filter} }}  # dynamically filter based on provided movieIds
        ?targetMovie movie:relatedTo ?sharedCastMember .
        ?otherMovie movie:relatedTo ?sharedCastMember .
        FILTER (?otherMovie != ?targetMovie)
    }}
    GROUP BY ?otherMovie
    HAVING (COUNT(DISTINCT ?targetMovie) = {target_movie_count}) #remove this if actors dont need to occur in both movies
    ORDER BY DESC(?sharedCount)
    """.format(movie_filter=movie_filter, target_movie_count=target_movie_count)

    moviesThatSharedActors = []
    for row in g.query(query):
        print(f"Other Movie: {row.otherMovie}, Shared Count: {row.sharedCount}")
        moviesThatSharedActors.append(row.otherMovie)


    for movie in moviesThatSharedActors:
        query = """
        SELECT DISTINCT ?sharedCastMember
        WHERE {{
            VALUES ?targetMovie {{ {movie_filter} }}  # dynamically filter based on provided movieIds
            ?targetMovie movie:relatedTo ?sharedCastMember .
            <{movie}> movie:relatedTo ?sharedCastMember . #custom other movie to get the actors that is being shared
        }}
        """.format(movie_filter=movie_filter, movie=movie)

        for row in g.query(query):
            print(f"Movie: {movie} Shared castmember: {row.sharedCastMember}")

    time.sleep(900000)