# SemanticProject

Movie Recommendation System


# Running Instructions

All these commands should be executed in the top-level `SemanticProject`.

## Step 1: Setup Jena Fuseki Server

Make sure you have java installed 
```bash
java --version
```

If not install java 
[Java](https://www.java.com/download/ie_manual.jsp.) 
Also install Java JDK23
[Java Development Kit 23](https://www.oracle.com/java/technologies/downloads/)

Then run the commands to start the Jena Fuseki Server for hosting the local knowledge graph

```bash
java -cp jena-fuseki-server-5.2.0.jar tdb2.tdbloader --loc=tdb2 model/graph/local_graph/complete_graph.ttl
```

LOAD AND START WITH POPULATED TDB2
```bash
java -jar jena-fuseki-server-5.2.0.jar --loc=tdb2 /dataset
```

## Step 1: Install Python and Libraries
Download Python and install all necessary Python libraries. This command will install the required libraries using `pip` and start the Flask server:
```bash
python setup.py
```
