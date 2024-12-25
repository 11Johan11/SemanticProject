from flask import Flask
from SPARQLWrapper import SPARQLWrapper, JSON
import json

app = Flask(__name__)
sparql = SPARQLWrapper(
    "https://query.wikidata.org/sparql"
)
sparql.setReturnFormat(JSON)

result = []

sparql.setQuery("""
    #Filmer som hade premiär 2017
    SELECT DISTINCT ?item ?itemLabel WHERE {
      ?item wdt:P31 wd:Q11424.
      ?item wdt:P577 ?pubdate.
      FILTER((?pubdate >= "2017-01-01T00:00:00Z"^^xsd:dateTime) && (?pubdate <= "2017-12-31T00:00:00Z"^^xsd:dateTime))
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
    }
    """
)



try:
    ret = sparql.queryAndConvert()

    for r in ret["results"]["bindings"]:
        result.append(r)
except Exception as e:
    print(e)

@app.route("/")
def hello_world():
    return json.dumps(result);

if __name__ == "__main__":
    app.run(debug=True)