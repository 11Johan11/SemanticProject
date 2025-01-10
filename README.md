# SemanticProject

Our main objective is to create a Movie Recommendation System utilizing SparQL and appropiate knowledge graphs such as Wikidata, And Infering some hidden relationships using rdfLIB. Fetching updated movie ratings from appropiate APIs, Using Flask to host the webpage


# Early Draft Plan
![DraftPlanMovieRecommendation](https://github.com/user-attachments/assets/e6c93107-1702-4d08-a403-dd82e9a140b9)


# Running Instructions

All these commands should be executed in the top-level `SemanticProject`.

## Step 1: Install Python and Libraries
Download Python and install all necessary Python libraries. This command will install the required libraries using `pip` and start the Flask server:
```bash
python setup.py
```

## Step 2: Setup Jena Fuseki Server

Make sure you have java installed 
```bash
java --version
```

If not install java [here](https://www.java.com/download/ie_manual.jsp.) 

Then run the commands to start the Jena Fuseki Server for hosting the local knowledge graph

```bash
java -cp jena-fuseki-server-5.2.0.jar tdb2.tdbloader --loc=tdb2 model/graph/local_graph/complete_graph.ttl
```

LOAD AND START WITH POPULATED TDB2
```bash
java -jar jena-fuseki-server-5.2.0.jar --loc=tdb2 /dataset
```