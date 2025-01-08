import json
import time
def calculate_movie_points(movie_data, extra_movie_data):
    # Extract publication years of inferred movies for comparison
    inferred_years = []
    for movie in extra_movie_data:
        inferred_years.append(int(movie["publicationDate"][:4]))

    def calculate_proximity_bonus(publication_year):
        # Award points based on closeness to the inferred years
        proximity_points = 0
        for inferred_year in inferred_years:
            year_difference = abs(publication_year - inferred_year)
            if year_difference <= 5:  # Close within 5 years gets higher points
                proximity_points += 20 - year_difference * 2  # Linear decrease
        return proximity_points

    recommended_movies = []

    for movie_uri, details in movie_data.items():
        points = 0

        # Points for shared movies
        points += details["originalSharedMovies"] * 10

        # Points for genres
        points += len(details.get("genres", [])) * 5

        # Points for actor popularity
        if len(details["actors"]) > 0:
            actor_points = sum(actor["popularity"] for actor in details.get("actors", [])) / len(details["actors"])
            points += actor_points

        # Calculate proximity bonus
        try:
            publication_year = int(details["publicationDate"][:4])
            #print(publication_year)
            proximity_points = calculate_proximity_bonus(publication_year)
            points += proximity_points
        except:
            pass

        recommended_movies.append({
            "title": details["title"],
            "movie_uri": movie_uri,
            "points": points,
            "shared_movies": details["sharedMovieUris"],
            "genres": [genre["name"] for genre in details.get("genres", [])],
            "actors": [{"name": actor["name"], "popularity": actor["popularity"]} for actor in details.get("actors", [])],
            "publicationDate": details.get("publicationDate")
        })

    # Sort movies by points (descending)
    recommended_movies.sort(key=lambda x: x["points"], reverse=True)

    #with open("recommended_movies.json", "w") as json_file:
        #json.dump(recommended_movies, json_file, indent=4)

    return recommended_movies