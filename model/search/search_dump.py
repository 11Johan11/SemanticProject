import time
from SPARQLWrapper import SPARQLWrapper, JSON
import json

#Fetch ALL Movie uris, Movie Titles, IMDB ids 
#Dump it into a JSON file for later use
#(used to optimize search and connect with TMDBP Api for movie posters)  (connecting made with IMDB id)
def search_dump():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setReturnFormat(JSON)
    query = """
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX wd: <http://www.wikidata.org/entity/> 
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX v: <http://www.wikidata.org/prop/statement/>

    SELECT ?q (SAMPLE(?movieName) AS ?movieName) WHERE {
      ?q wdt:P31 wd:Q11424.       #instance of a film (series/movies so on)
      #?q wdt:P345 ?imdb.          #must have an IMDb ID

      #attempt to fetch the english label
      OPTIONAL { ?q rdfs:label ?movieNameEn. FILTER(LANG(?movieNameEn) = "en") }
      
      #fallback to any available label
      OPTIONAL { ?q rdfs:label ?movieNameFallback. }

      #prioritize english label if available, otherwise use fallback
      BIND(COALESCE(?movieNameEn, ?movieNameFallback) AS ?movieName)
    }
    GROUP BY ?q ?imdb
    """
    try:
        #setup
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        #execute and store results
        ret = sparql.queryAndConvert()
        results = ret["results"]["bindings"]

        #dump results to a JSON file so we can reuse it and dont no unnecessary calls
        with open("search_movie_dump.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

        print("Results successfully saved to 'search_movie_dump.json'.")
    except Exception as e:
        #(e.g., too many requests, timeout)
        print("An error occurred:", e)

print("hey")
search_dump()