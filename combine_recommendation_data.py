from model.graph.infer import infer_shared_actors, infer_shared_genres, fetch_and_map_actor_metadata, filter_actor_popularity, fetch_and_map_director_metadata, infer_shared_directors, fetch_movie_data, fetch_movies_from_actors, fetch_movies_from_directors
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



i want you to fix and combine this, so just add like wishedActor´and the other data and make sure to combine it properly:
its from this: actor_movies = fetch_movies_from_actors(list_of_actors)
{"http://www.wikidata.org/entity/Q1049139": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Spy Game"}, "http://www.wikidata.org/entity/Q107040798": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "The Lost City"}, "http://www.wikidata.org/entity/Q107119206": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Babylon"}, "http://www.wikidata.org/entity/Q1119322": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Exit Through the Gift Shop"}, "http://www.wikidata.org/entity/Q1127709": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "True Romance"}, "http://www.wikidata.org/entity/Q114246242": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "F1"}, "http://www.wikidata.org/entity/Q1145732": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Sleepers"}, "http://www.wikidata.org/entity/Q116470707": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Wolfs"}, "http://www.wikidata.org/entity/Q12124934": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Hunk"}, "http://www.wikidata.org/entity/Q1263003": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "The Favor"}, "http://www.wikidata.org/entity/Q136264": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Killing Them Softly"}, "http://www.wikidata.org/entity/Q1432710": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Full Frontal"}, "http://www.wikidata.org/entity/Q14786561": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Fury"}, "http://www.wikidata.org/entity/Q153723": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Inglourious Basterds"}, "http://www.wikidata.org/entity/Q167051": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "The Dark Side of the Sun"}, "http://www.wikidata.org/entity/Q175038": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "12 Monkeys"}, "http://www.wikidata.org/entity/Q179798": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Kalifornia"}, "http://www.wikidata.org/entity/Q17986183": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "By the Sea"}, "http://www.wikidata.org/entity/Q183239": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "The Curious Case of Benjamin Button"}, "http://www.wikidata.org/entity/Q186587": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Troy"}, "http://www.wikidata.org/entity/Q190050": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Fight Club"}, "http://www.wikidata.org/entity/Q190908": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Seven"}, "http://www.wikidata.org/entity/Q191040": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Mr. & Mrs. Smith"}, "http://www.wikidata.org/entity/Q191074": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Babel"}, "http://www.wikidata.org/entity/Q19850715": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "The Big Short"}, "http://www.wikidata.org/entity/Q1988803": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Happy Together"}, "http://www.wikidata.org/entity/Q205447": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Ocean's Eleven"}, "http://www.wikidata.org/entity/Q21463782": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "War Machine"}, "http://www.wikidata.org/entity/Q221820": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Moneyball"}, "http://www.wikidata.org/entity/Q2359049": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Johnny Suede"}, "http://www.wikidata.org/entity/Q2364033": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Cutting Class"}, "http://www.wikidata.org/entity/Q23681360": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Allied"}, "http://www.wikidata.org/entity/Q23707679": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Voyage of Time"}, "http://www.wikidata.org/entity/Q244257": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "The Tree of Life"}, "http://www.wikidata.org/entity/Q25394556": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Touch of Evil"}, "http://www.wikidata.org/entity/Q25431158": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Deadpool 2"}, "http://www.wikidata.org/entity/Q26265": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Cool World"}, "http://www.wikidata.org/entity/Q28196": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "World War Z"}, "http://www.wikidata.org/entity/Q2992335": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Across the Tracks"}, "http://www.wikidata.org/entity/Q3023357": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "12 Years a Slave"}, "http://www.wikidata.org/entity/Q3061599": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "The Counselor"}, "http://www.wikidata.org/entity/Q318910": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Interview with the Vampire"}, "http://www.wikidata.org/entity/Q335160": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Snatch"}, "http://www.wikidata.org/entity/Q381731": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Burn After Reading"}, "http://www.wikidata.org/entity/Q38774788": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Ad Astra"}, "http://www.wikidata.org/entity/Q388950": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "The Assassination of Jesse James by the Coward Robert Ford"}, "http://www.wikidata.org/entity/Q403830": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Less Than Zero"}, "http://www.wikidata.org/entity/Q431708": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "No Man's Land"}, "http://www.wikidata.org/entity/Q45082723": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Bad Boy Kummer"}, "http://www.wikidata.org/entity/Q4664493": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Abby Singer"}, "http://www.wikidata.org/entity/Q469839": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "The Mexican"}, "http://www.wikidata.org/entity/Q47300912": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Once Upon a Time in Hollywood"}, "http://www.wikidata.org/entity/Q504053": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Ocean's Twelve"}, "http://www.wikidata.org/entity/Q5164779": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Contact"}, "http://www.wikidata.org/entity/Q521094": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "The Devil's Own"}, "http://www.wikidata.org/entity/Q581906": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "A River Runs Through It"}, "http://www.wikidata.org/entity/Q635632": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Ocean's Thirteen"}, "http://www.wikidata.org/entity/Q649165": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Being John Malkovich"}, "http://www.wikidata.org/entity/Q658041": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Thelma & Louise"}, "http://www.wikidata.org/entity/Q676513": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Meet Joe Black"}, "http://www.wikidata.org/entity/Q770965": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Confessions of a Dangerous Mind"}, "http://www.wikidata.org/entity/Q7769248": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "The Tiger"}, "http://www.wikidata.org/entity/Q844883": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Seven Years in Tibet"}, "http://www.wikidata.org/entity/Q913324": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Legends of the Fall"}, "http://www.wikidata.org/entity/Q99900595": {"wishedActor": "http://www.wikidata.org/entity/Q35332", "wishedActorName": "Brad Pitt", "movieName": "Bullet Train"}, "http://www.wikidata.org/entity/Q105482844": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Pinocchio"}, "http://www.wikidata.org/entity/Q106428": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Apollo 13"}, "http://www.wikidata.org/entity/Q107167": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Sleepless in Seattle"}, "http://www.wikidata.org/entity/Q108086029": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Asteroid City"}, "http://www.wikidata.org/entity/Q111608782": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "A Man Called Otto"}, "http://www.wikidata.org/entity/Q112054756": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Here"}, "http://www.wikidata.org/entity/Q1127184": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Splash"}, "http://www.wikidata.org/entity/Q11343993": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Extraordinary Voyage"}, "http://www.wikidata.org/entity/Q1161624": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Man with One Red Shoe"}, "http://www.wikidata.org/entity/Q12128282": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Radio Flyer"}, "http://www.wikidata.org/entity/Q1306472": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "A League of Their Own"}, "http://www.wikidata.org/entity/Q1334320": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Elvis Has Left the Building"}, "http://www.wikidata.org/entity/Q134773": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Forrest Gump"}, "http://www.wikidata.org/entity/Q1537568": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Turner & Hooch"}, "http://www.wikidata.org/entity/Q160560": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Da Vinci Code"}, "http://www.wikidata.org/entity/Q16251439": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "A Hologram for the King"}, "http://www.wikidata.org/entity/Q165817": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Saving Private Ryan"}, "http://www.wikidata.org/entity/Q1740544": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The 'Burbs"}, "http://www.wikidata.org/entity/Q1740645": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Joe Versus the Volcano"}, "http://www.wikidata.org/entity/Q1747149": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Great Buck Howard"}, "http://www.wikidata.org/entity/Q1781116": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Nothing in Common"}, "http://www.wikidata.org/entity/Q1786324": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Volunteers"}, "http://www.wikidata.org/entity/Q18067135": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Bridge of Spies"}, "http://www.wikidata.org/entity/Q18151148": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Ithaca"}, "http://www.wikidata.org/entity/Q18192306": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Inferno"}, "http://www.wikidata.org/entity/Q192934": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Angels & Demons"}, "http://www.wikidata.org/entity/Q1961600": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Punchline"}, "http://www.wikidata.org/entity/Q204057": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Philadelphia"}, "http://www.wikidata.org/entity/Q208108": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Catch Me If You Can"}, "http://www.wikidata.org/entity/Q208263": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Green Mile"}, "http://www.wikidata.org/entity/Q21010849": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Circle"}, "http://www.wikidata.org/entity/Q21062112": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Sully"}, "http://www.wikidata.org/entity/Q213411": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Cast Away"}, "http://www.wikidata.org/entity/Q2244246": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Pixar Story"}, "http://www.wikidata.org/entity/Q24635346": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Defying the Nazis: The Sharps' War"}, "http://www.wikidata.org/entity/Q26863800": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "California Typewriter"}, "http://www.wikidata.org/entity/Q273568": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Charlie Wilson's War"}, "http://www.wikidata.org/entity/Q284229": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "You've Got Mail"}, "http://www.wikidata.org/entity/Q28936": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Cloud Atlas"}, "http://www.wikidata.org/entity/Q2937646": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Captain Phillips"}, "http://www.wikidata.org/entity/Q30203425": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Post"}, "http://www.wikidata.org/entity/Q3029511": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "He Knows You're Alone"}, "http://www.wikidata.org/entity/Q3061506": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Every Time We Say Goodbye"}, "http://www.wikidata.org/entity/Q318766": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Terminal"}, "http://www.wikidata.org/entity/Q3474574": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Saving Mr. Banks"}, "http://www.wikidata.org/entity/Q382864": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Larry Crowne"}, "http://www.wikidata.org/entity/Q389014": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Dragnet"}, "http://www.wikidata.org/entity/Q468033": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Road to Perdition"}, "http://www.wikidata.org/entity/Q50404285": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Greyhound"}, "http://www.wikidata.org/entity/Q5158515": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Concert for George"}, "http://www.wikidata.org/entity/Q535096": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Celluloid Closet (film)"}, "http://www.wikidata.org/entity/Q55605492": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Finch"}, "http://www.wikidata.org/entity/Q56244787": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Barbra: The Concert"}, "http://www.wikidata.org/entity/Q56703347": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "A Beautiful Day in the Neighborhood"}, "http://www.wikidata.org/entity/Q642410": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "That Thing You Do!"}, "http://www.wikidata.org/entity/Q730473": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Bonfire of the Vanities"}, "http://www.wikidata.org/entity/Q7317370": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Return with Honor"}, "http://www.wikidata.org/entity/Q73537408": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "News of the World"}, "http://www.wikidata.org/entity/Q798133": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Bachelor Party"}, "http://www.wikidata.org/entity/Q82426": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Prohibition"}, "http://www.wikidata.org/entity/Q83739": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Ladykillers"}, "http://www.wikidata.org/entity/Q84362533": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Elvis"}, "http://www.wikidata.org/entity/Q858467": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Big"}, "http://www.wikidata.org/entity/Q862197": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Polar Express"}, "http://www.wikidata.org/entity/Q918769": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Extremely Loud and Incredibly Close"}, "http://www.wikidata.org/entity/Q969651": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "The Money Pit"}, "http://www.wikidata.org/entity/Q99671372": {"wishedActor": "http://www.wikidata.org/entity/Q2263", "wishedActorName": "Tom Hanks", "movieName": "Borat Subsequent Moviefilm"}}
"""
def extract_id_from_uri(uri):
    return uri.split("/")[-1]
def combine_recommendation_data(list_of_movies, list_of_actors, list_of_directors):
    # Fetch and process data for shared actors

    actor_movies = fetch_movies_from_actors(list_of_actors)

    director_movies = fetch_movies_from_directors(list_of_directors)

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


    #WISHED ACTORS
    # Process wished actors
    for movie_uri, data in actor_movies.items():
        wished_actors = data.get("wishedActors", [])
        if not wished_actors:
            continue

        if movie_uri not in shared_results:
            shared_results[movie_uri] = {"shared_result": []}

        for wished_actor in wished_actors:
            add_shared_result(
                movie_uri,
                [movie_uri],  # Only include the specific movie as shared
                {
                    "wishedActor": [wished_actor["wishedActorName"]],
                    "wishedActorUri": [wished_actor["wishedActorUri"]],
                },
            )

    # Process wished directors
    for movie_uri, data in director_movies.items():
        wished_directors = data.get("wishedDirectors", [])
        if not wished_directors:
            continue

        if movie_uri not in shared_results:
            shared_results[movie_uri] = {"shared_result": []}

        for wished_director in wished_directors:
            add_shared_result(
                movie_uri,
                [movie_uri],  # Only include the specific movie as shared
                {
                    "wishedDirector": [wished_director["wishedDirectorName"]],
                    "wishedDirectorUri": [wished_director["wishedDirectorUri"]],
                },
            )


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


  
    #with open("johan.json", "w", encoding="utf-8") as file:
        #json.dump(shared_results, file, ensure_ascii=False, indent=2)


    """
},
  "http://www.wikidata.org/entity/Q16704857": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q1405126",
          "Q163872",
          "Q172241",
          "Q44578"
        ],
        "common": {
          "genres": [
            "drama film"
          ]
        }
      }
    ],
    "title": "Лера",
    "publicationDate": "2007-01-01",
    "imdbId": "tt3498014"
  },
  "http://www.wikidata.org/entity/Q167051": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q1405126",
          "Q163872",
          "Q172241",
          "Q44578"
        ],
        "common": {
          "genres": [
            "drama film",
            "romance film"
          ]
        }
      },
      {
        "sharedMovies": [
          "Q163872",
          "Q1405126",
          "Q172241",
          "Q44578"
        ],
        "common": {
          "wishedActor": [
            "Brad Pitt"
          ],
          "wishedActorUri": [
            "http://www.wikidata.org/entity/Q35332"
          ]
        }
      }
    ],
    "title": "The Dark Side of the Sun",
    "publicationDate": "1988-01-01",
    "imdbId": "tt0118930"
  },
  "http://www.wikidata.org/entity/Q1670513": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q1405126",
          "Q163872",
          "Q172241",
          "Q44578"
        ],
        "common": {
          "genres": [
            "drama film"
          ]
        }
      }
    ],
    "title": "Sunshine State",
    "publicationDate": "2002-01-01",
    "imdbId": "tt0286179"
  },
  "http://www.wikidata.org/entity/Q16705797": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q1405126",
          "Q163872",
          "Q172241",
          "Q44578"
        ],
        "common": {
          "genres": [
            "drama film"
          ]
        }
      }
    ],
    "title": "Summer's Children",
    "publicationDate": "1979-01-01",
    "imdbId": "tt0088203"
  },
  "http://www.wikidata.org/entity/Q16706317": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q1405126",
          "Q163872",
          "Q172241",
          "Q44578"
        ],
        "common": {
          "genres": [
            "drama film"
          ]
        }
      }
    ],
    "title": "Whispering Pages",
    "publicationDate": "1994-01-01",
    "imdbId": "tt0108338"
  },
  "http://www.wikidata.org/entity/Q16707610": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q1405126",
          "Q163872",
          "Q172241",
          "Q44578"
        ],
        "common": {
          "genres": [
            "drama film",
            "historical film"
          ]
        }
      }
    ],
    "title": "Her Name Was Fanny Kaplan",
    "publicationDate": "2016-07-19",
    "imdbId": "tt5017008"
  },
  "http://www.wikidata.org/entity/Q1670780": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q1405126",
          "Q163872",
          "Q172241",
          "Q44578"
        ],
        "common": {
          "genres": [
            "drama film"
          ]
        }
      }
    ],
    "title": "The Substance of Fire",
    "publicationDate": "1997-01-01",
    "imdbId": "tt0117773"
  },
  "http://www.wikidata.org/entity/Q16707866": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q1405126",
          "Q163872",
          "Q172241",
          "Q44578"
        ],
        "common": {
          "genres": [
            "drama film"
          ]
        }
      }
    ],
    "title": "Une lettre ne s'écrit pas",
    "publicationDate": "2013-01-01",
    "imdbId": "tt2375735"
  },
  "http://www.wikidata.org/entity/Q16708461": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q1405126",
          "Q163872",
          "Q172241",
          "Q44578"
        ],
        "common": {
          "genres": [
            "drama film"
          ]
        }
      }
    ],
    "title": "In the Line of Duty: Blaze of Glory",
    "publicationDate": "1997-01-01",
    "imdbId": "tt0119363"
  },
  "http://www.wikidata.org/entity/Q1670881": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q1405126",
          "Q163872",
          "Q172241",
          "Q44578"
        ],
        "common": {
          "genres": [
            "drama film"
          ]
        }
      }
    ],
    "title": "Oberstadtgass",
    "publicationDate": "1956-01-01",
    "imdbId": "tt0049566"
  },
  "http://www.wikidata.org/entity/Q167092": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q1405126",
          "Q163872",
          "Q172241",
          "Q44578"
        ],
        "common": {
          "genres": [
            "drama film"
          ]
        }
      }
    ],
    "title": "Snowed In",
    "publicationDate": "1926-01-01",
    "imdbId": "tt0017408"
  },
  "http://www.wikidata.org/entity/Q16711026": {
    "shared_result": [
      {
        "sharedMovies": [
          "Q1405126",
          "Q163872",
          "Q172241",
          "Q44578"
        ],
        "common": {
          "genres": [
            "drama film"
          ]
        }
      }
    ],



    """

    #time.sleep(999999)



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