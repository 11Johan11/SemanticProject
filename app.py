from flask import Flask, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS
import owlrl  # For reasoning
import json
import time

from model.sparql.get_director_and_their_movies import get_director_and_their_movies
from model.sparql.get_cast_members_and_their_movies import get_cast_members_and_their_movies
from model.sparql.get_genres_and_their_movies import get_genres_and_their_movies
results = []
results = get_director_and_their_movies(["Q153723"])

# Create RDFLib graph
g = Graph()
MOVIE = Namespace("http://example.org/movie#")
g.bind("movie", MOVIE)

for result in results:
    movie_uri = URIRef(result["otherMovie"]["value"])
    movie_title = Literal(result["otherMovieName"]["value"])

    director_uri = URIRef(result["director"]["value"])
    director_name = Literal(result["directorName"]["value"])

    g.add((movie_uri, RDF.type, MOVIE.Movie))
    g.add((movie_uri, MOVIE.title, movie_title))

    g.add((movie_uri, MOVIE.director, director_uri)) #Director type

    g.add((director_uri, MOVIE.name, director_name))
    g.add((director_uri, RDF.type, MOVIE.Person)) #perhaps not needed but good for future usecase

results = get_cast_members_and_their_movies(["Q153723"])
#print(json.dumps(results))
for result in results:
    movie_uri = URIRef(result["otherMovie"]["value"])
    movie_title = Literal(result["otherMovieName"]["value"])

    cast_member_uri = URIRef(result["castMember"]["value"])
    cast_member_name = Literal(result["castMemberName"]["value"])

    g.add((movie_uri, RDF.type, MOVIE.Movie))
    g.add((movie_uri, MOVIE.title, movie_title))

    g.add((movie_uri, MOVIE.castmember, cast_member_uri)) #Castmember type

    g.add((cast_member_uri, MOVIE.name, cast_member_name))
    g.add((cast_member_uri, RDF.type, MOVIE.Person)) #perhaps not needed but good for future usecase

# Add reasoning rules/ontology
#g.add((MOVIE.director, RDFS.subPropertyOf, MOVIE.relatedTo))
g.add((MOVIE.castmember, RDFS.subPropertyOf, MOVIE.relatedTo))

# Apply reasoning
owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)


# Query the graph for inferred relationships
query = """
SELECT DISTINCT ?movie1 ?movie2 ?person
WHERE {
    ?movie1 movie:relatedTo ?person .
    ?movie2 movie:relatedTo ?person .
    FILTER (?movie1 != ?movie2)
}
"""
inferred_results = []
for row in g.query(query):
    inferred_results.append({
        "movie1": str(row.movie1),
        "movie2": str(row.movie2),
        "related": str(row.person)
    })

print(inferred_results)

time.sleep(900000)

app = Flask(__name__)

# SPARQL setup
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)

# Define namespaces
MOVIE = Namespace("http://example.org/movie#")
PERSON = Namespace("http://example.org/person#")
#inglorious bastards https://www.wikidata.org/wiki/Q338002
#fury https://www.wikidata.org/wiki/Q14786561
#downfal https://www.wikidata.org/wiki/Q152857
@app.route('/movies2017', methods=['GET'])
def get_movies():
    #hämta alla filmer
    sparql.setQuery("""
        SELECT DISTINCT ?item ?itemLabel ?pubdate WHERE {
          ?item wdt:P31 wd:Q11424.
          ?item wdt:P577 ?pubdate.
          FILTER((?pubdate >= "2017-01-01T00:00:00Z"^^xsd:dateTime) && (?pubdate <= "2017-01-20T00:00:00Z"^^xsd:dateTime))
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
        }
    """)

    try:
        # Fetch results from SPARQL
        ret = sparql.queryAndConvert()
        results = ret["results"]["bindings"]

        # Create RDFLib graph
        g = Graph()
        g.bind("movie", MOVIE)

        # Add movies to the graph
        for result in results:
            movie_uri = URIRef(result["item"]["value"])
            movie_label = Literal(result["itemLabel"]["value"])
            pub_date = Literal(result["pubdate"]["value"])

            g.add((movie_uri, RDF.type, MOVIE.Movie))
            g.add((movie_uri, MOVIE.label, movie_label))
            g.add((movie_uri, MOVIE.releaseDate, pub_date))

        # Add reasoning rules/ontology
        g.add((MOVIE.directedBy, RDFS.subPropertyOf, MOVIE.relatedTo))
        g.add((MOVIE.releaseDate, RDFS.subPropertyOf, MOVIE.relatedTo))

        # Add some example data to demonstrate reasoning
        example_director = URIRef("http://example.org/person#Director1")
        g.add((example_director, RDF.type, MOVIE.Person))
        g.add((example_director, MOVIE.directedBy, URIRef("http://example.org/movie#Movie1")))

        # Apply reasoning
        owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)

        # Query the graph for inferred relationships
        query = """
        SELECT ?movie ?related WHERE {
            ?movie <http://example.org/movie#relatedTo> ?related.
        }
        """
        inferred_results = []
        for row in g.query(query):
            inferred_results.append({
                "movie": str(row.movie),
                "related": str(row.related)
            })

        return jsonify(inferred_results)

    except Exception as e:
        return jsonify({"error": str(e)})

#get inglorious bastards movie, get the composers name also


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



@app.route('/hanslanda')
def hans_landa():
    try:
        sparql.setQuery("""
SELECT ?movies ?director ?directorName ?moviesNames WHERE {
  ##wd:Q338002 ?property ?value.
  #SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,fr,ar,be,bg,bn,ca,cs,da,de,el,en,es,et,fa,fi,he,hi,hu,hy,id,it,ja,jv,ko,nb,nl,eo,pa,pl,pt,ro,ru,sh,sk,sr,sv,sw,te,th,tr,uk,yue,vec,vi,zh". }
  OPTIONAL { wd:Q153723 wdt:P86 ?composer. }
  #OPTIONAL { ?composer rdfs:label ?composerName. }
  #?movie wdt:P86 ?composer. #go backwards and fetch all the movies for that composer 
  
  wd:Q153723 wdt:P57 ?director.
  ?director rdfs:label ?directorName.
  ?movies wdt:P57 ?director.
  ?movies wdt:P1476 ?moviesNames.
  
  FILTER (lang(?directorName) = "en") #keep only english (otherwise there will be a ton)
  FILTER (lang(?moviesNames) = "en")
}""")
        ret = sparql.queryAndConvert()
        results = ret["results"]["bindings"]
        return(json.dumps(results))
    except Exception as e:
        return(e)

if __name__ == '__main__':
    app.run(debug=True)