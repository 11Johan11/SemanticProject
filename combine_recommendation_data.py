from model.graph.infer import infer_shared_actors, infer_shared_genres, fetch_and_map_actor_metadata, filter_actor_popularity, fetch_and_map_director_metadata, infer_shared_directors, fetch_movie_data
import json
import time


"""

MOVIES THAT SHARED ACTORS STRUCTURE
{
  "http://www.wikidata.org/entity/Q1049139": {
    "originalSharedMovies": 2,
    "sharedMovieUris": [
      "http://www.wikidata.org/entity/Q153723",
      "http://www.wikidata.org/entity/Q14786561"
    ],
    "actors": [
      {
        "uri": "http://www.wikidata.org/entity/Q35332",
        "name": "Brad Pitt",
        "profile": "https://image.tmdb.org/t/p/original//4rjnRCQ6bGFYdBb4UooOjsQy12c.jpg",
        "popularity": 91.226
      }
    ]
  },
  "http://www.wikidata.org/entity/Q107040798": {
    "originalSharedMovies": 2,
    "sharedMovieUris": [
      "http://www.wikidata.org/entity/Q153723",
      "http://www.wikidata.org/entity/Q14786561"
    ],
    "actors": [
      {
        "uri": "http://www.wikidata.org/entity/Q35332",
        "name": "Brad Pitt",
        "profile": "https://image.tmdb.org/t/p/original//4rjnRCQ6bGFYdBb4UooOjsQy12c.jpg",
        "popularity": 91.226
      }
    ]
  },


MOVIES THAT SHARED DIRECTORS STRUCTURE
{
  "http://www.wikidata.org/entity/Q104123": {
    "originalSharedMovies": 1,
    "sharedMovieUris": [
      "http://www.wikidata.org/entity/Q153723"
    ],
    "directors": [
      {
        "uri": "http://www.wikidata.org/entity/Q3772",
        "name": "Quentin Tarantino",
        "profile": "https://image.tmdb.org/t/p/original//1gjcpAa99FAOWGnrUvHEXXsRs7o.jpg",
        "popularity": 57.15
      }
    ]
  },
  "http://www.wikidata.org/entity/Q1137310": {
    "originalSharedMovies": 1,
    "sharedMovieUris": [
      "http://www.wikidata.org/entity/Q153723"
    ],
    "directors": [
      {
        "uri": "http://www.wikidata.org/entity/Q3772",
        "name": "Quentin Tarantino",
        "profile": "https://image.tmdb.org/t/p/original//1gjcpAa99FAOWGnrUvHEXXsRs7o.jpg",
        "popularity": 57.15
      }
    ]
  },

  MOVIES THAT SHARED GENRES STRUCTURE 

  {
  "http://www.wikidata.org/entity/Q1000094": {
    "title": "You're Dead",
    "originalSharedMovies": 2,
    "sharedMovieUris": [
      "http://www.wikidata.org/entity/Q496654",
      "http://www.wikidata.org/entity/Q1345077"
    ],
    "genres": [
      {
        "uri": "http://www.wikidata.org/entity/Q157443",
        "name": "comedy film"
      }
    ]
  },
  "http://www.wikidata.org/entity/Q10007277": {
    "title": "Pacho, hybský zbojník",
    "originalSharedMovies": 2,
    "sharedMovieUris": [
      "http://www.wikidata.org/entity/Q496654",
      "http://www.wikidata.org/entity/Q1345077"
    ],
    "genres": [
      {
        "uri": "http://www.wikidata.org/entity/Q157443",
        "name": "comedy film"
      }
    ]
  },
"""
def extract_id_from_uri(uri):
    return uri.split("/")[-1]
def combine_recommendation_data(list_of_movies):
    # Fetch and process data for shared actors

    print("Infering actors....")
    shared_actor_data = filter_actor_popularity(
        fetch_and_map_actor_metadata(infer_shared_actors(list_of_movies)),
        threshold=30
    )

    print("Infering directors...")
    # Fetch and process data for shared directors
    shared_director_data = fetch_and_map_director_metadata(
        infer_shared_directors(list_of_movies)
    )
    print("Infering shared genres..")
    # Fetch and process data for shared genres
    shared_genre_data = infer_shared_genres(list_of_movies)

    shared_results = {}

    def normalize_shared_movies(shared_movies):
        return tuple(sorted(shared_movies))

    def add_shared_result(movie_uri, shared_movies, common_data):
        shared_movies_key = normalize_shared_movies(shared_movies)

        if movie_uri not in shared_results:
            shared_results[movie_uri] = {
                #"title": None,  # Title can be fetched if needed
                "shared_result": []
            }

        for result in shared_results[movie_uri]["shared_result"]:
            if result["sharedMovies"] == list(shared_movies_key):
                for key, value in common_data.items():
                    result["common"].setdefault(key, []).extend(value)
                return

        shared_results[movie_uri]["shared_result"].append({
            "sharedMovies": list(shared_movies_key),
            "common": common_data
        })

    for movie_uri, data in shared_actor_data.items():
        shared_movies = [extract_id_from_uri(uri) for uri in data.get("sharedMovieUris", [])]
        actors = [actor["name"] for actor in data.get("actors", [])]
        if shared_movies:
            add_shared_result(movie_uri, shared_movies, {"actors": actors})

    for movie_uri, data in shared_director_data.items():
        shared_movies = [extract_id_from_uri(uri) for uri in data.get("sharedMovieUris", [])]
        directors = [director["name"] for director in data.get("directors", [])]
        if shared_movies:
            add_shared_result(movie_uri, shared_movies, {"directors": directors})

    for movie_uri, data in shared_genre_data.items():
        shared_movies = [extract_id_from_uri(uri) for uri in data.get("sharedMovieUris", [])]
        genres = [genre["name"] for genre in data.get("genres", [])]
        if shared_movies:
            add_shared_result(movie_uri, shared_movies, {"genres": genres})



    new_list_of_movies = []
    for uri, data in shared_results.items():
        new_list_of_movies.append(extract_id_from_uri(uri))

    print("Fetch other moviedata (titel,publicationdate etc....)")
    movie_data = fetch_movie_data(new_list_of_movies) 

    for uri, data in shared_results.items():
        try:
            shared_results[uri]["title"] = movie_data[uri]["title"]
            shared_results[uri]["publicationDate"] = movie_data[uri]["publicationDate"]
            shared_results[uri]["imdbId"] = movie_data[uri]["imdbId"]
        except:
            pass

    movie_data_for_target_movies = fetch_movie_data(list_of_movies) 


  
    with open("johan.json", "w", encoding="utf-8") as file:
        json.dump(shared_results, file, ensure_ascii=False, indent=2)




    return shared_results, movie_data_for_target_movies
"""     
example on how i want it

"inferring on movie1 & movie2"

    "movie_that_shared_uri":
            title: b¨labla, 
            "shared_result":      
                [{"sharedMovies": ["movie1","movie2"],"genres": ["comedy"],"actors": ["brad pitt"]} #shared comedy and brad pit with both movies
                {"sharedMovies": ["movie2"],"genres": ["action"],"actors": ["brad pitt"]}, #shared brad pitt with movie2 and shared action with movie2
                {"sharedMovies": ["movie1"],"director": ["quentin tarantino"]}, #shared director with movie 1

                ]  ALSO VERY IMPORTANT that  "sharedMovies": ["movie1","movie2"] <=> "sharedMovies": ["movie2","movie1"]
    
    print("Combining data...")
    # Combine the data into a single dictionary
    combined_data = {}
    
    # Process actors
    for uri, data in shared_actor_data.items():
        if uri not in combined_data:
            combined_data[uri] = {
                "title": data["title"],
                "originalSharedMovies": data["originalSharedMovies"],
                "sharedMovieUris": data["sharedMovieUris"],
                "actors": data.get("actors", []),
                "directors": [],
                "genres": []
            }
        combined_data[uri]["actors"].extend(data.get("actors", []))

    # Process directors
    for uri, data in shared_director_data.items():
        if uri not in combined_data:
            combined_data[uri] = {
                "title": data["title"],
                "originalSharedMovies": data["originalSharedMovies"],
                "sharedMovieUris": data["sharedMovieUris"],
                "actors": [],
                "directors": data.get("directors", []),
                "genres": []
            }
        combined_data[uri]["directors"].extend(data.get("directors", []))

    # Process genres
    for uri, data in shared_genre_data.items():
        if uri not in combined_data:
            combined_data[uri] = {
                "title": data["title"],
                "originalSharedMovies": data["originalSharedMovies"],
                "sharedMovieUris": data["sharedMovieUris"],
                "actors": [],
                "directors": [],
                "genres": data.get("genres", [])
            }
        combined_data[uri]["genres"].extend(data.get("genres", []))
    """


"""
    shit_list = []
    for uri, data in combined_data.items():
        shit_list.append(extract_id_from_uri(uri))


    date_data = fetch_publicationdate(shit_list)
    date_data_dict = {item["movie"]: item["publicationDate"] for item in date_data}

    for uri, data in combined_data.items():
        try:
            combined_data[uri]["publicationDate"] = date_data_dict[uri]
        except:
            pass

    print("Fetch publicationdates...")
    original_movie_data = fetch_publicationdate(list_of_movies) 

    
    # Write the combined data to a JSON file
    #output_file = "shared_data.json"
    #with open(output_file, "w", encoding="utf-8") as file:
        #json.dump(combined_data, file, ensure_ascii=False, indent=2)
    #output_file = "original_movie_data.json"       




    #with open(output_file, "w", encoding="utf-8") as file:
        #json.dump(original_movie_data, file, ensure_ascii=False, indent=2)

    #print(f"Combined data written to {output_file}")
    return {"shared_actors": shared_actor_data, "shared_directors": shared_director_data, "shared_genres": shared_genre_data}, original_movie_data
    """