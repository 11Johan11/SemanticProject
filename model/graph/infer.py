from model.graph.init import init_graph 
import owlrl
import time
from model.search.main import add_person_metadata
import time
import json

def infer_shared_actors(movie_ids):
    g = init_graph()  #load our local graph
    print("Starting to reason...")

    target_movie_count = len(movie_ids)
    movie_filter = " ".join(f"wd:{movie}" for movie in movie_ids)

    # ↓↓↓ REMOVED LINE ↓↓↓
    # HAVING (COUNT(DISTINCT ?targetMovie) = {target_movie_count}) #remove this if actors dont need to occur in both movies
    query = """
    SELECT DISTINCT ?sharedCastMember ?otherMovie (COUNT(DISTINCT ?sharedCastMember) AS ?sharedCount)
    WHERE {{
        VALUES ?targetMovie {{ {movie_filter} }}
        ?targetMovie wdt:P161 ?sharedCastMember .
        ?otherMovie wdt:P161 ?sharedCastMember .
        FILTER (?otherMovie != ?targetMovie)
    }}
    GROUP BY ?otherMovie
    ORDER BY DESC(?sharedCount)
    """.format(movie_filter=movie_filter, target_movie_count=target_movie_count)

    moviesThatSharedActors = []
    for row in g.query(query):
        # ↓↓↓ ADDED originalSharedMovies ↓↓↓
        moviesThatSharedActors.append({
            "movie": str(row.otherMovie),
            "originalSharedMovies": int(row.sharedCount)
        })

    # ↓↓↓ CHANGED structure to include originalSharedMovies ↓↓↓
    popularity_over_30_actors = {}
    for entry in moviesThatSharedActors:
        popularity_over_30_actors[entry["movie"]] = {
            "originalSharedMovies": entry["originalSharedMovies"],
            "actors": []
        }
        query = """
        SELECT DISTINCT ?sharedCastMember ?sharedCastMemberName
        WHERE {{
            VALUES ?targetMovie {{ {movie_filter} }}
            ?targetMovie wdt:P161 ?sharedCastMember .
            ?sharedCastMember rdfs:label ?sharedCastMemberName .
            <{movie}> wdt:P161 ?sharedCastMember .
        }}
        """.format(movie_filter=movie_filter, movie=entry["movie"])

        for row in g.query(query):
            popularity_over_30_actors[entry["movie"]]["actors"].append({
                "uri": row.sharedCastMember,
                "name": row.sharedCastMemberName
            })

    return popularity_over_30_actors



def get_actors_over_30_popularity(movies_with_actors, THRESHOLD=30):
    actor_info_map = {}

    for movie, cast_list in movies_with_actors.items():
        # CHANGED: to handle both dict/list for 'cast_list'
        # If it's a dict (with "actors"), use cast_list["actors"]
        # Otherwise, assume it's already a list of dicts
        if isinstance(cast_list, dict) and "actors" in cast_list:  # ADDED
            cast_list = cast_list["actors"]                       # ADDED

        for castmember in cast_list:
            # If castmember is not a dict, skip it
            if not isinstance(castmember, dict):  # ADDED
                continue                          # ADDED
            uri_str = str(castmember["uri"])
            name_str = castmember.get("name", "")
            actor_info_map[uri_str] = {
                "uri": uri_str,
                "name": name_str
            }

    # ADDED: Define all_actor_list for add_person_metadata
    all_actor_list = [{"uri": key} for key in actor_info_map.keys()]

    for info in add_person_metadata(all_actor_list):
        uri = str(info["uri"])
        popularity = info.get("popularity", 0)
        profile = info.get("profile", "")
        if uri in actor_info_map:
            actor_info_map[uri]["popularity"] = popularity
            actor_info_map[uri]["profile"] = profile

    # CHANGED: movies_with_actors_and_popularity can hold originalSharedMovies + actors
    movies_with_actors_and_popularity = {
        movie: {
            "originalSharedMovies": 0,  # default 0
            "actors": []
        }
        for movie in movies_with_actors.keys()
    }

    for movie, cast_list in movies_with_actors.items():
        # If cast_list is dict and contains 'originalSharedMovies', copy that value
        if isinstance(cast_list, dict) and "originalSharedMovies" in cast_list:  # ADDED
            movies_with_actors_and_popularity[movie]["originalSharedMovies"] = cast_list["originalSharedMovies"]  # ADDED
            cast_list = cast_list["actors"]  # ADDED

        # If cast_list is not a list, skip
        if not isinstance(cast_list, list):  # ADDED
            continue

        for castmember in cast_list:
            if not isinstance(castmember, dict):  # ADDED
                continue
            uri_str = str(castmember["uri"])
            actor_data = actor_info_map.get(uri_str)
            if actor_data and actor_data.get("popularity", 0) >= THRESHOLD:
                movies_with_actors_and_popularity[movie]["actors"].append(actor_data)

    movies_with_actors_and_popularity = sorted(
        movies_with_actors_and_popularity.items(),
        key=lambda x: len(x[1]["actors"]),
        reverse=True
    )
    movies_with_actors_and_popularity = dict(movies_with_actors_and_popularity)

    with open('movies_with_actors_and_popularity.json', 'w') as json_file:
        json.dump(movies_with_actors_and_popularity, json_file, indent=4)

    time.sleep(999999)
    return movies_with_actors_and_popularity


def infer_shared_genres(movie_ids):
    g = init_graph() 

    #apply reasoning
    #owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)   

    target_movie_count = len(movie_ids)

    movie_filter = " ".join(f"wd:{movie}" for movie in movie_ids)

    print(movie_filter)
    #Count shared genres for specific movie(s)
    query = """
    SELECT DISTINCT ?sharedGenre ?otherMovie (COUNT(DISTINCT ?sharedGenre) AS ?sharedCount)
    WHERE {{
        VALUES ?targetMovie {{ {movie_filter} }}  # dynamically filter based on provided movieIds
        ?targetMovie wdt:P136 ?sharedGenre . 
        ?otherMovie wdt:P136 ?sharedGenre .
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
 