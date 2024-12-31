import requests
import json
import time

#TMDB API
#use backdrop path for movie poster
url = "https://api.themoviedb.org/3/find/tt0361748?external_source=imdb_id"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4N2NhYWVlZjk5OTRlZTIxNDk3ZDA1Mzc0ZTg1ODdiYSIsIm5iZiI6MTczNTU3NDYwMy44OTQsInN1YiI6IjY3NzJjNDRiNjIzNGMxYjQ2ZjYxNGU3ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.7jM6UhZJFYPblmV8e-UE5QzvjT8Nl1TA5jvebToAZFg"
}

response = requests.get(url, headers=headers)
data = json.loads(response.text)
poster_path = data["movie_results"][0]["poster_path"]
image_url = f"https://image.tmdb.org/t/p/original/{poster_path}"
ratings = data["movie_results"][0]["vote_average"]
print(ratings)
#{'movie_results': [{'backdrop_path': '/1Jpkm9qZcsT0mSyVXgs4VlGjPNI.jpg', 'id': 16869, 'title': 'Inglourious Basterds', 'original_title': 'Inglourious Basterds', 'overview': 'In Nazi-occupied France during World War II, a group of Jewish-American soldiers known as "The Basterds" are chosen specifically to spread fear throughout the Third Reich by scalping and brutally killing Nazis. The Basterds, lead by Lt. Aldo Raine soon cross paths with a French-Jewish teenage girl who runs a movie theater in Paris which is targeted by the soldiers.', 'poster_path': '/7sfbEnaARXDDhKm0CZ7D7uc2sbo.jpg', 'media_type': 'movie', 'adult': False, 'original_language': 'en', 'genre_ids': [18, 53, 10752], 'popularity': 93.655, 'release_date': '2009-08-02', 'video': False, 'vote_average': 8.2, 'vote_count': 22318}], 'person_results': [], 'tv_results': [], 'tv_episode_results': [], 'tv_season_results': []}
