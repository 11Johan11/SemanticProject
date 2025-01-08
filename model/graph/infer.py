from model.graph.init import init_graph 
import owlrl
import time
from model.search.main import add_person_metadata
import time
import json

#todo perhaps if there's > 5 target movies dont bother fetching for movies with distinct target movie = 1? HAVING (COUNT(DISTINCT ?targetMovie) > 1)
def infer_shared_actors(movie_ids):
    g = init_graph()  # Load our local graph
    print("Starting to reason...")

    target_movie_count = len(movie_ids)
    movie_filter = " ".join(f"wd:{movie}" for movie in movie_ids)

    # Main query to fetch shared actors, counts, and target movie URIs
    query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT DISTINCT ?sharedCastMember ?otherMovie (COUNT(DISTINCT ?targetMovie) AS ?originalSharedMovies) 
                   (GROUP_CONCAT(DISTINCT ?targetMovie; separator=",") AS ?sharedMovieUris)
    WHERE {{
        VALUES ?targetMovie {{ {movie_filter} }}
        ?targetMovie wdt:P161 ?sharedCastMember .
        ?otherMovie wdt:P161 ?sharedCastMember .
        FILTER (?otherMovie != ?targetMovie) 
    }}
    GROUP BY ?sharedCastMember ?otherMovie
    ORDER BY DESC(?originalSharedMovies)
    """

    moviesThatSharedActors = []
    for row in g.query(query):
        moviesThatSharedActors.append({
            "movie": str(row.otherMovie),
            "originalSharedMovies": int(row.originalSharedMovies),  # Store the count
            "sharedMovieUris": str(row.sharedMovieUris).split(",")  # Split URIs into a list
        })

    # Structure to include originalSharedMovies, sharedMovieUris, and shared actors
    movies_with_shared_actors = {}
    for entry in moviesThatSharedActors:
        movies_with_shared_actors[entry["movie"]] = {
            "originalSharedMovies": entry["originalSharedMovies"],
            "sharedMovieUris": entry["sharedMovieUris"],  # Add shared movie URIs
            "actors": []
        }
        query = f"""
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            
        SELECT DISTINCT ?sharedCastMember ?sharedCastMemberName
        WHERE {{
            VALUES ?targetMovie {{ {movie_filter} }}
            ?targetMovie wdt:P161 ?sharedCastMember .
            ?sharedCastMember rdfs:label ?sharedCastMemberName .
            <{entry["movie"]}> wdt:P161 ?sharedCastMember .
        }}
        """
        for row in g.query(query):
            movies_with_shared_actors[entry["movie"]]["actors"].append({
                "uri": row.sharedCastMember,
                "name": row.sharedCastMemberName
            })

    #print(json.dumps(movies_with_shared_actors, indent=2))
    #time.sleep(9999999)
    return movies_with_shared_actors

"""
structure that add_pers
[
    {
        "uri": "http://www.wikidata.org/entity/Q3607626",
    },
    {
        "uri": "http://www.wikidata.org/entity/Q329178"
    }
]

actor_metadata = [{"uri": "http://www.wikidata.org/entity/Q4957491", "popularity": 1.508, "profile": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Unknown_person.jpg"}, {"uri": "http://www.wikidata.org/entity/Q382523", "popularity": 1.495, "profile": "https://image.tmdb.org/t/p/original//uIyS0Rx2hDJNBBSoC3wQH49FXVi.jpg"}, {"uri": "http://www.wikidata.org/entity/Q2850927", "popularity": 1.48, "profile": "https://image.tmdb.org/t/p/original//p2uX1gxUt8BNBPT1f0UsUQDpogZ.jpg"}, {"uri": "http://www.wikidata.org/entity/Q2003843", "popularity": 1.38, "profile": "https://image.tmdb.org/t/p/original//wNle9vJfQmhJONZA8SdQbVZMqJh.jpg"}, {"uri": "http://www.wikidata.org/entity/Q15434786", "popularity": 1.323, "profile": "https://image.tmdb.org/t/p/original//88gHRiuIhFunoytQuobkzmDIaIc.jpg"}, {"uri": "http://www.wikidata.org/entity/Q20685594", "popularity": 0.045, "profile": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Unknown_person.jpg"}, {"uri": "http://www.wikidata.org/entity/Q1514600", "popularity": 0, "profile": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Unknown_person.jpg"}, {"uri": "http://www.wikidata.org/entity/Q5345686", "popularity": 0, "profile": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Unknown_person.jpg"}]

"""

def fetch_and_map_actor_metadata(movies_with_shared_actors):
    all_actor_uris = []
    unique_uris = set()  #to ensure unique uris (no duplicates)

    for movie_data in movies_with_shared_actors.values():
        for actor in movie_data["actors"]:
            actor_uri = str(actor["uri"])
            if actor_uri not in unique_uris:
                all_actor_uris.append({"uri": actor_uri})
                unique_uris.add(actor_uri)

    #fetch all metadata using add_person_metadata
    actor_metadata = add_person_metadata(all_actor_uris)

    #convert metadata to a dictionary for faster lookup
    metadata_dict = {entry["uri"]: entry for entry in actor_metadata}

    #map metadata back to the original structure
    for movie, movie_data in movies_with_shared_actors.items():
        for actor in movie_data["actors"]:
            metadata = metadata_dict.get(str(actor["uri"]), {})
            actor["profile"] = metadata.get("profile", "")
            actor["popularity"] = metadata.get("popularity", 0)

    movies_with_shared_actors_metadata = movies_with_shared_actors

    return movies_with_shared_actors_metadata


def filter_actor_popularity(movies_with_shared_actors_metadata, threshold=30):
    # Filtered result dictionary
    filtered_movies = {}

    for movie_uri, movie_data in movies_with_shared_actors_metadata.items():
        # Filter actors in the current movie based on popularity
        movie_data["actors"] = [actor for actor in movie_data["actors"] if actor["popularity"] >= threshold]

        # Only include the movie if it has remaining actors
        if movie_data["actors"]:
            filtered_movies[movie_uri] = movie_data

    return filtered_movies


def infer_shared_genres(movie_ids, output_file="shared_genres.json"):

    g = init_graph()  # Load our local graph

    movie_filter = " ".join(f"wd:{movie}" for movie in movie_ids)

    # Combined query to fetch all relevant data in one go
    query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
       
    SELECT DISTINCT ?otherMovie ?sharedGenre ?sharedGenreName (COUNT(DISTINCT ?targetMovie) AS ?originalSharedMovies) 
                   (GROUP_CONCAT(DISTINCT ?targetMovie; separator=",") AS ?sharedMovieUris)
    WHERE {{
        VALUES ?targetMovie {{ {movie_filter} }}
        ?targetMovie wdt:P136 ?sharedGenre .
        ?otherMovie wdt:P136 ?sharedGenre .
        ?sharedGenre rdfs:label ?sharedGenreName .
        FILTER (?otherMovie != ?targetMovie)
    }}
    GROUP BY ?otherMovie ?sharedGenre ?sharedGenreName
    ORDER BY DESC(?originalSharedMovies)
    """

    print("Running combined query...")
    results = []
    for row in g.query(query):
        results.append({
            "movie": str(row.otherMovie),
            "genre_uri": str(row.sharedGenre),
            "genre_name": str(row.sharedGenreName),
            "originalSharedMovies": int(row.originalSharedMovies),
            "sharedMovieUris": str(row.sharedMovieUris).split(",")
        })

    # Process results into the desired structure
    print("Processing combined results...")
    movies_with_shared_genres = {}
    for result in results:
        movie = result["movie"]
        if movie not in movies_with_shared_genres:
            movies_with_shared_genres[movie] = {
                "originalSharedMovies": result["originalSharedMovies"],
                "sharedMovieUris": result["sharedMovieUris"],
                "genres": []
            }
        movies_with_shared_genres[movie]["genres"].append({
            "uri": result["genre_uri"],
            "name": result["genre_name"]
        })

    # Save the result to a JSON file
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(movies_with_shared_genres, file, ensure_ascii=False, indent=2)

    print(f"Results saved to {output_file}")
    return movies_with_shared_genres

