from model.graph.infer import infer_shared_actors, infer_shared_genres, fetch_and_map_actor_metadata, filter_actor_popularity, fetch_and_map_director_metadata, infer_shared_directors, fetch_publicationdate
import json
import time
def extract_id_from_uri(uri):
    return uri.split("/")[-1]
def combine_recommendation_data(list_of_movies):
    # Fetch and process data for shared actors
    shared_actor_data = filter_actor_popularity(
        fetch_and_map_actor_metadata(infer_shared_actors(list_of_movies)),
        threshold=30
    )
    # Fetch and process data for shared directors
    shared_director_data = fetch_and_map_director_metadata(
        infer_shared_directors(list_of_movies)
    )
    # Fetch and process data for shared genres
    shared_genre_data = infer_shared_genres(list_of_movies)


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


    
    # Write the combined data to a JSON file
    #output_file = "shared_data.json"
    #with open(output_file, "w", encoding="utf-8") as file:
        #json.dump(combined_data, file, ensure_ascii=False, indent=2)
    #output_file = "original_movie_data.json"       

    original_movie_data = fetch_publicationdate(list_of_movies) 
    #with open(output_file, "w", encoding="utf-8") as file:
        #json.dump(original_movie_data, file, ensure_ascii=False, indent=2)

    #print(f"Combined data written to {output_file}")
    return combined_data, original_movie_data