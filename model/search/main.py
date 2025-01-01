import requests
import json
import time
#from fuzzywuzzy import fuzz
from rapidfuzz import fuzz


#TODO: perhaps if the similarity score is below 70 dont even bother fetching metadata/including in search results?
#Search the datadump, fuzz allows typos
def search(query, threshold=70, limit=30, minChar=3):
   
    if len(query) < minChar:
        return "Query must contain at least 3 characters."

    print("Loading data...")
    with open("search_movie_dump.json", "r", encoding="utf-8") as f:
        searchable_movies = json.load(f)
    print(len(searchable_movies))
    results = []
    print("Searching....")
    for entry in searchable_movies:
        #if c == limit:
            #break

        try:
            title = entry["movieName"]["value"]
            uri = entry["q"]["value"]
        except:
            continue

        #fuzzy matching
        #similarity_score = fuzz.partial_ratio(query.lower(), title.lower())
        similarity_score = fuzz.token_set_ratio(query.lower(), title.lower())

        #threshold for inclusivity (100 perfect match etc...)
        length_penalty = (abs(len(query) - len(title)) / max(len(query), len(title))) * 0.5
        adjusted_score = similarity_score * (1 - length_penalty)
        if adjusted_score > threshold:
            results.append({"title": title, "score": adjusted_score, "uri": uri})
                    

    #sort results by similarity score in descending order
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:limit]


def extract_id_from_uri(uri):
    return uri.split("/")[-1]

#Appends movie poster image path, ratings (TMDB ratings), media_type 
def add_movie_metadata(search_results):

    #TMDB API
    #use backdrop path for movie poster

    session = requests.Session()  #session (faster than reopening the connection each time)
    session.headers.update({
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4N2NhYWVlZjk5OTRlZTIxNDk3ZDA1Mzc0ZTg1ODdiYSIsIm5iZiI6MTczNTU3NDYwMy44OTQsInN1YiI6IjY3NzJjNDRiNjIzNGMxYjQ2ZjYxNGU3ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.7jM6UhZJFYPblmV8e-UE5QzvjT8Nl1TA5jvebToAZFg"
    })

    new_search_results = []
    for entry in search_results:
        wikidata_id = extract_id_from_uri(entry["uri"])

        url = f"https://api.themoviedb.org/3/find/{wikidata_id}?external_source=wikidata_id"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4N2NhYWVlZjk5OTRlZTIxNDk3ZDA1Mzc0ZTg1ODdiYSIsIm5iZiI6MTczNTU3NDYwMy44OTQsInN1YiI6IjY3NzJjNDRiNjIzNGMxYjQ2ZjYxNGU3ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.7jM6UhZJFYPblmV8e-UE5QzvjT8Nl1TA5jvebToAZFg"
        }

        response = session.get(url) #TODO: handle connection limit/error etc...
        #response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        try: 
            poster_path = data["movie_results"][0]["poster_path"]
            image_url = f"https://image.tmdb.org/t/p/original/{poster_path}"

            entry["ratings"] = data["movie_results"][0]["vote_average"]
            entry["media_type"] = data["movie_results"][0]["media_type"]
            entry["popularity"] = data["movie_results"][0]["popularity"]
            entry["poster"] = image_url
        except:
            entry["ratings"] = "0"
            entry["media_type"] = "movie"
            entry["poster"] = "https://media.istockphoto.com/id/995815438/vector/movie-and-film-modern-retro-vintage-poster-background.jpg?s=612x612&w=0&k=20&c=UvRsJaKcp0EKIuqDKp6S7Dwhltt0D5rbegPkS-B8nDQ="

        new_search_results.append(entry)
        new_search_results = sorted(new_search_results, key=lambda x: x.get("popularity", 0), reverse=True) #sort by popularity aswell
        print(entry["ratings"])
    return new_search_results

#Example usage
#query = "avengers"
#search_results = search(query)
#add_move_metadata(search_results)

"""
{
  "movie_results": [
    {
      "backdrop_path": "/hpQ7dLKEdIsztIIFUMzrgVZMkls.jpg",
      "id": 42756,
      "title": "Angels Over Broadway",
      "original_title": "Angels Over Broadway",
      "overview": "Small-time businessman Charles Engle is threatened with exposure for embezzling $3,000 for his free-spending wife. Deciding on suicide, he scribbles a note, stuffs it in his pocket and goes for one last night on the town. He is pulled into a poker game by conman Bill O'Brien and singer Nina Barone, but when they discover the dropped note, they resolve to turn the tables, get Engle his $3,000 and save his life.",
      "poster_path": "/nee1LVYfgKE6fWrXNzi94fl2PAR.jpg",
      "media_type": "movie",
      "adult": false,
      "original_language": "en",
      "genre_ids": [
        18,
        80
      ],
      "popularity": 3.521,
      "release_date": "1940-10-02",
      "video": false,
      "vote_average": 5.8,
      "vote_count": 27
    }
  ],
  "person_results": [],
  "tv_results": [],
  "tv_episode_results": [],
  "tv_season_results": []
}
"""