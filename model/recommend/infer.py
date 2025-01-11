from model.local_graph.init import init
import owlrl
import time
from model.search.main import add_person_metadata
import time
import json

#todo perhaps if there's > 5 target movies dont bother fetching for movies with distinct target movie = 1? HAVING (COUNT(DISTINCT ?targetMovie) > 1)
#infer shared directors just like actos its wdt:P57
def infer_shared_actors(movie_ids,g):
    print("Starting to reason...")

    target_movie_count = len(movie_ids)
    movie_filter = " ".join(f"wd:{movie}" for movie in movie_ids)

    query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT DISTINCT ?sharedCastMember ?sharedCastMemberName ?otherMovie 
                   (COUNT(DISTINCT ?targetMovie) AS ?originalSharedMovies) 
                   (GROUP_CONCAT(DISTINCT ?targetMovie; separator=",") AS ?sharedMovieUris)
    WHERE {{
        VALUES ?targetMovie {{ {movie_filter} }}
        ?targetMovie wdt:P161 ?sharedCastMember .
        ?sharedCastMember rdfs:label ?sharedCastMemberName .
        ?otherMovie wdt:P161 ?sharedCastMember .
        FILTER (?otherMovie != ?targetMovie) 
    }}
    GROUP BY ?sharedCastMember ?sharedCastMemberName ?otherMovie
    ORDER BY DESC(?originalSharedMovies)
    """


    movies_with_shared_actors = {}
    for row in g.query(query):
        other_movie = str(row.otherMovie)
        shared_cast_member = str(row.sharedCastMember)
        shared_cast_member_name = str(row.sharedCastMemberName)
        original_shared_movies = int(row.originalSharedMovies)
        shared_movie_uris = str(row.sharedMovieUris).split(",")
        #other_movie_name = str(row.otherMovieName)

        if other_movie not in movies_with_shared_actors:
            movies_with_shared_actors[other_movie] = {
                #"title": other_movie_name,
                "originalSharedMovies": original_shared_movies,
                "sharedMovieUris": shared_movie_uris,
                "actors": []
            }

        movies_with_shared_actors[other_movie]["actors"].append({
            "uri": shared_cast_member,
            "name": shared_cast_member_name
        })

    return movies_with_shared_actors


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
    filtered_movies = {}

    for movie_uri, movie_data in movies_with_shared_actors_metadata.items():
        movie_data["actors"] = [actor for actor in movie_data["actors"] if actor["popularity"] >= threshold]
        if movie_data["actors"]:
            filtered_movies[movie_uri] = movie_data

    return filtered_movies


def infer_shared_directors(movie_ids,g):
    print("Starting to reason...")

    target_movie_count = len(movie_ids)
    movie_filter = " ".join(f"wd:{movie}" for movie in movie_ids)

    query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT DISTINCT ?sharedDirector ?sharedDirectorName ?otherMovie ?otherMovieName
                   (COUNT(DISTINCT ?targetMovie) AS ?originalSharedMovies) 
                   (GROUP_CONCAT(DISTINCT ?targetMovie; separator=",") AS ?sharedMovieUris)
    WHERE {{
        VALUES ?targetMovie {{ {movie_filter} }}
        ?targetMovie wdt:P57 ?sharedDirector .
        ?sharedDirector rdfs:label ?sharedDirectorName .
        ?otherMovie wdt:P57 ?sharedDirector .
        ?otherMovie rdfs:label ?otherMovieName .
        FILTER (?otherMovie != ?targetMovie) 
    }}
    GROUP BY ?sharedDirector ?sharedDirectorName ?otherMovie ?otherMovieName
    ORDER BY DESC(?originalSharedMovies)
    """

    movies_with_shared_directors = {}
    for row in g.query(query):
        other_movie = str(row.otherMovie)
        shared_director = str(row.sharedDirector)
        shared_director_name = str(row.sharedDirectorName)
        original_shared_movies = int(row.originalSharedMovies)
        shared_movie_uris = str(row.sharedMovieUris).split(",")
        other_movie_name = str(row.otherMovieName)

        if other_movie not in movies_with_shared_directors:
            movies_with_shared_directors[other_movie] = {
                "title": other_movie_name,
                "originalSharedMovies": original_shared_movies,
                "sharedMovieUris": shared_movie_uris,
                "directors": []
            }

        movies_with_shared_directors[other_movie]["directors"].append({
            "uri": shared_director,
            "name": shared_director_name
        })

    return movies_with_shared_directors

def fetch_and_map_director_metadata(movies_with_shared_directors):
    all_director_uris = []
    unique_uris = set()  #to ensure unique URIs (no duplicates)

    for movie_data in movies_with_shared_directors.values():
        for director in movie_data["directors"]:
            director_uri = str(director["uri"])
            if director_uri not in unique_uris:
                all_director_uris.append({"uri": director_uri})
                unique_uris.add(director_uri)

    director_metadata = add_person_metadata(all_director_uris)

    #convert metadata to a dictionary for faster lookup
    metadata_dict = {entry["uri"]: entry for entry in director_metadata}

    # Map metadata back to the original structure
    for movie, movie_data in movies_with_shared_directors.items():
        for director in movie_data["directors"]:
            metadata = metadata_dict.get(str(director["uri"]), {})
            director["profile"] = metadata.get("profile", "")
            director["popularity"] = metadata.get("popularity", 0)

    movies_with_shared_directors_metadata = movies_with_shared_directors

    return movies_with_shared_directors_metadata



def infer_shared_genres(movie_ids, g):

    movie_filter = " ".join(f"wd:{movie}" for movie in movie_ids)

    #combined query to fetch all relevant data in one go, #?sharedGenreName (COUNT(DISTINCT ?targetMovie) AS ?originalSharedMovies) 
    query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
       
    SELECT DISTINCT ?otherMovie ?sharedGenre ?sharedGenreName
                   (GROUP_CONCAT(DISTINCT ?targetMovie; separator=",") AS ?sharedMovieUris)
    WHERE {{
        VALUES ?targetMovie {{ {movie_filter} }}
        ?targetMovie wdt:P136 ?sharedGenre .
        ?otherMovie wdt:P136 ?sharedGenre .
        ?sharedGenre rdfs:label ?sharedGenreName .
        FILTER (?otherMovie != ?targetMovie)
    }}
    GROUP BY ?otherMovie ?otherMovieName ?sharedGenre ?sharedGenreName
    ORDER BY DESC(?originalSharedMovies)
    """

    print("Running combined query...")
    results = []
    for row in g.query(query):
        results.append({
            #"title": str(row.otherMovieName),
            "movie": str(row.otherMovie),
            "genre_uri": str(row.sharedGenre),
            "genre_name": str(row.sharedGenreName),
            #"originalSharedMovies": int(row.originalSharedMovies),
            "sharedMovieUris": str(row.sharedMovieUris).split(",")
        })

    print("Processing combined results...")
    movies_with_shared_genres = {}
    for result in results:
        movie = result["movie"]
        if movie not in movies_with_shared_genres:
            movies_with_shared_genres[movie] = {
                #"title": result["title"],
                #"originalSharedMovies": result["originalSharedMovies"],
                "sharedMovieUris": result["sharedMovieUris"],
                "genres": []
            }
        movies_with_shared_genres[movie]["genres"].append({
            "uri": result["genre_uri"],
            "name": result["genre_name"]
        })

    # Save the result to a JSON file
    #with open(output_file, "w", encoding="utf-8") as file:
        #json.dump(movies_with_shared_genres, file, ensure_ascii=False, indent=2)

    #print(f"Results saved to {output_file}")
    return movies_with_shared_genres

def fetch_movie_data(movie_ids,g):
    movie_filter = " ".join(f"wd:{movie}" for movie in movie_ids)
    
    query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
    
    SELECT DISTINCT ?targetMovie ?publicationDate ?imdbId ?title {{
        VALUES ?targetMovie {{ {movie_filter} }}
        ?targetMovie wdt:P577 ?publicationDate.
        ?targetMovie wdt:P345 ?imdbId.
        ?targetMovie rdfs:label ?title.

    }}
    """

    results = {}

    for row in g.query(query):
        #format the publicationDate as YYYY-MM-DD
        #try:
        raw_date = str(row.publicationDate)
        formatted_date = raw_date.split("T")[0]  #extract date portion before 'T'
        #except:
       

        results[str(row.targetMovie)] = {
            "publicationDate": formatted_date,
            "title": str(row.title),
            "imdbId": str(row.imdbId)
        }
    return results



def fetch_movies_from_actors(actor_ids,g):
    actor_filter = " ".join(f"wd:{actor}" for actor in actor_ids)
    
    query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
    
    SELECT DISTINCT ?movie ?movieName ?actor ?actorName {{
        VALUES ?actor {{ {actor_filter} }}
        ?movie wdt:P161 ?actor.
        ?movie rdfs:label ?movieName.
        ?actor rdfs:label ?actorName.
    }}
    """

    results = {}

    for row in g.query(query):
        movie_uri = str(row.movie)
        actor_uri = str(row.actor)
        actor_name = str(row.actorName)
        
        if movie_uri not in results:
            results[movie_uri] = {
                "wishedActors": [],
                #"movieName": str(row.movieName)
            }

        results[movie_uri]["wishedActors"].append({
            "wishedActorUri": actor_uri,
            "wishedActorName": actor_name
        })

    return results


def fetch_movies_from_directors(director_ids,g):
    director_filter = " ".join(f"wd:{director}" for director in director_ids)
    
    query = f"""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
    
    SELECT DISTINCT ?movie ?movieName ?director ?directorName {{
        VALUES ?director {{ {director_filter} }}
        ?movie wdt:P57 ?director.
        ?movie rdfs:label ?movieName.
        ?director rdfs:label ?directorName.
    }}
    """

    results = {}

    for row in g.query(query):
        movie_uri = str(row.movie)
        director_uri = str(row.director)
        director_name = str(row.directorName)
        
        if movie_uri not in results:
            results[movie_uri] = {
                "wishedDirectors": [],  #Initialize a list to store multiple directors!!!
                #"movieName": str(row.movieName)  # Uncomment if needed
            }

        results[movie_uri]["wishedDirectors"].append({
            "wishedDirectorUri": director_uri,
            "wishedDirectorName": director_name
        })

    return results    
#def fetch_everything(movie_ids):
