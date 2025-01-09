import json
import time


"""
okay so now i want to calculate movie points, so this one here below is old and is not compatible with the new shared_results which you helped me very kindly with,
I want you to make this calculate movie points compatible with the shared_results

as a reminder this is how the datastructure looks like

  "http://www.wikidata.org/entity/Q1595582": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q496654"
        ],
        "common": {
          "actors": [
            "Sean Astin"
          ],
          "genres": [
            "comedy film"
          ]
        }
      }
    ],
    "title": "The Last Producer",
    "publicationDate": "2000-01-01",
    "imdbId": "tt0201726"
  },
  "http://www.wikidata.org/entity/Q15985322": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q496654"
        ],
        "common": {
          "actors": [
            "Terry Crews"
          ]
        }
      }
    ],
    "title": "Draft Day",
    "publicationDate": "2014-04-11",
    "imdbId": "tt2223990"
  },
  "http://www.wikidata.org/entity/Q1601681": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q496654"
        ],
        "common": {
          "actors": [
            "Sean Astin"
          ]
        }
      }
    ],
    "title": "The Final Season",
    "publicationDate": "2007-01-01",
    "imdbId": "tt0449018"
  },
  "http://www.wikidata.org/entity/Q1612502": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q496654"
        ],
        "common": {
          "actors": [
            "James Earl Jones"
          ],
          "genres": [
            "fantasy film"
          ]
        }
      }
    ],
    "title": "The Flight of Dragons",
    "publicationDate": "1982-01-01",
    "imdbId": "tt0083951"
  },
  "http://www.wikidata.org/entity/Q16156329": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q496654"
        ],
        "common": {
          "actors": [
            "Kate Beckinsale",
            "Brian Cox"
          ]
        }
      },
      {
        "sharedMovies": [
          "Q17182905",
          "Q496654"
        ],
        "common": {
          "genres": [
            "science fiction film",
            "comedy film"
          ]
        }
      }
    ],



but i want you to basically do something similiar here but be very clever, like if there's two shared movies, for one genre, that movie gets the double amount of points than
if there was like one movie that shared that genre, but i basicallly also want you to setup weights, how much it should double per shared movie for each type, like actor/genres/directors

but be very clever, and also ofcourse calculate some distance between the target movies, but for example


so the input (movie_data, movie_data_for_target_movies)

movie_data is the datastrcuture json we talked about above

movie_data_for_target_movies is some extra data for the sharedMovies
{'http://www.wikidata.org/entity/Q496654': {'publicationDate': '2006-06-22', 'title': 'Click', 'imdbId': 'tt0389860'}, 'http://www.wikidata.org/entity/Q17182905': {'publicationDate': '2015-07-25', 'title': 'Pixels', 'imdbId': 'tt2120120'}}

And for now, i only want you to calculate like a distance so like the target movies is 2006 and 2015 so i dont know but be clever so it should be distributevly get extra points for staying in that close range

good luck!





 "http://www.wikidata.org/entity/Q1004433": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q496654",
          "Q56312570"
        ],
        "common": {
          "actors": [
            "Adam Sandler"
          ],
          "wishedActor": "Adam Sandler",
          "wishedActorUri": "http://www.wikidata.org/entity/Q132952"
        }
      },
      {
        "sharedMovies": [
          "Q496654"
        ],
        "common": {
          "genres": [
            "comedy film"
          ]
        }
      }
    ],

"""
def calculate_movie_points(movie_data, movie_data_for_target_movies):
    # Define weights
    WEIGHTS = {
        "actors": 10,
        "genres": 5,
        "directors": 15,
        "wishedActor": 30,
        "wishedDirector": 30
    }

    # Extract publication years of target movies
    target_years = [
        int(movie_data_for_target_movies[movie]["publicationDate"].split("-")[0])
        for movie in movie_data_for_target_movies
    ]

    def calculate_proximity_bonus(publication_year):
        # Award points based on closeness to target years
        proximity_points = 0
        for target_year in target_years:
            year_difference = abs(publication_year - target_year)
            if year_difference <= 5:  # Close within 5 years gets higher points
                proximity_points += 20 - year_difference * 2  # Linear decrease
        return proximity_points

    recommended_movies = []

    for movie_uri, details in movie_data.items():
        points = 0

        for shared_entry in details.get("shared_result", []):
            shared_movies = shared_entry["sharedMovies"]
            common = shared_entry["common"]

            for category, items in common.items():
                if category in WEIGHTS:
                    multiplier = len(shared_movies)  # More shared movies, higher weight
                    points += len(items) * WEIGHTS[category] * multiplier




        # Calculate proximity bonus
        try:
            publication_year = int(details.get("publicationDate", "0").split("-")[0])
            points += calculate_proximity_bonus(publication_year)
        except ValueError:
            pass

        recommended_movies.append({
            "title": details.get("title"),
            "imdbId": details.get("imdbId"),
            "movie_uri": movie_uri,
            "points": points,
            "shared_result": details.get("shared_result"),
            "publicationDate": details.get("publicationDate")
        })

    # Sort movies by points (descending)
    recommended_movies.sort(key=lambda x: x["points"], reverse=True)

    #with open("johan_recommended_movies.json", "w", encoding="utf-8") as file:
        #json.dump(recommended_movies, file, ensure_ascii=False, indent=2)    

    #TODO: perhaps also add actors uris
    #time.sleep(99999)

    return recommended_movies