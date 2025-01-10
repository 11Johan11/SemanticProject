# SemanticProject

Movie Recommendation System

Using a knowledge graph running on Jena Fuseki to infer relationships between movies

# Rerunning Instructions

All these commands should be executed in the top-level `SemanticProject`.

## Step 1: Setup Jena Fuseki Server

Make sure you have Java and JDK23 installed

```bash
java --version
```

If not, install Java from (https://www.java.com/sv/download/) and also install Java JDK23 from (https://www.oracle.com/java/technologies/downloads/).

Then run the commands to start the Jena Fuseki Server for hosting the local knowledge graph. This command will load and export the `.ttl` file into a TDB2 format, which is a high-performance storage format used by Apache Jena for persisting RDF data.

```bash
java -cp jena-fuseki-server-5.2.0.jar tdb2.tdbloader --loc=tdb2 model/graph/local_graph/complete_graph.ttl
```

Start Jena Fuseki Server and load the TDB2 dataset

```bash
java -jar jena-fuseki-server-5.2.0.jar --loc=tdb2 /dataset
```

## Step 2: Install Python and Libraries

Download Python and install all necessary Python libraries. This command will install the required libraries using `pip` and start the Flask server:

```bash
python setup.py
```

