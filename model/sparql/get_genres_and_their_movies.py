from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS
import json
#P57 Director
#P161 Cast Member
#P136 Genre
#P577 Publication Date
#P162 Producer
#P1431 Executive Producer
#P58 Screenwriter
#P144 Based On
#P495 Country Of Origin
#P915 Filming Location
#P840 Narrative Location
#P344 Director of Photography
#P345 IMDB ID
#P2408 Set in period
#P2047 Duration
#P1040 Film editor
#P921 Main subject
#P750 Distributed by
#P2515 Costume designer
#P2554 Production Designer
#P2142 Box office
#P2208 Average shot length
#P2755 Exploitation Mark Number
#P3803 Original Film Format
#P3816 Film Script
#P1476 Title
#P676 lyricist
#P364 Original Language 
#P166 Award Received
#P8345 Media Franchise
#P179 Part of the series
#P2769 Budget
#P272 Production Company
#P4805 Make up artist
#P2130 Capital cost
#P462 Color
#P1258 Rotten Tomatoes ID
#P1411 Nominated for

#setup for sparql
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)

#Helper function (extract the entity id from a uri)
#Example http://www.wikidata.org/entity/Q3772 --> Q3772
def extract_id_from_uri(uri):
    return uri.split("/")[-1]

def get_genres_and_their_movies(movie_ids):

    movie_filter = " ".join(f"wd:{movie}" for movie in movie_ids) 

    query = """
    SELECT ?otherMovie ?otherMovieName ?genre ?genreName WHERE {{
      VALUES ?originalMovie {{ {movie_filter} }}  #dynamically filter based on provided movieIds
      
      #Get genre of the original movies
      ?originalMovie wdt:P136 ?genre.
      #?originalMovie wdt:P1476 ?moviesNames. not used, we already know the target movie's name
      ?genre rdfs:label ?genreName.
      FILTER (lang(?genreName) = "en")
  
      #Get other movies with the same genres
      ?otherMovie wdt:P136 ?genre.

      #attempt to fetch the english label
      OPTIONAL {{ ?otherMovie rdfs:label ?movieNameEn. FILTER(LANG(?movieNameEn) = "en") }}
      #fallback to any available label
      OPTIONAL {{ ?otherMovie rdfs:label ?movieNameFallback. }}
      #prioritize english label if available, otherwise use fallback
      BIND(COALESCE(?movieNameEn, ?movieNameFallback) AS ?otherMovieName) 

      
    }}
    """.format(movie_filter=movie_filter)

    #print(query)

    try:
        sparql.setQuery(query)

        ret = sparql.queryAndConvert()
        results = ret["results"]["bindings"]

        #print(json.dumps(results))
        return results
    except Exception as e:
        #TODO: Handle too many requests, timeout/retry etc... 
        print(e)


#print(get_genres_and_their_movies(["Q153723"])) #Inglorious Bastards "Q153723" and Fury "Q14786561"