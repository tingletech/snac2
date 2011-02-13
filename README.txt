eac-load-graph
==============

a process to create a directed, attributed, edge-labeled, multi-graph of
social networks derived from processing archival context records

Data files
----------

data 			- EAC_DIR  - symbolic link to EAC files
graph-snac-example.xml	- GRAPH_ML - graphML file
neo4j-db 		- GRAPH_DB - neo4j database created by load_*.grm scripts

Load scripts
------------

load/load_eac.grm	- process EAC_DIR and creates GRAPH_ML and GRAPH_DB
load/load_graphml.grm 	- process GRAPH_ML and creates GRAPH_DB


Gremlin
-------
pull_gremlin.bash	- checkout and build gremlin
gremlin			- gremlin git repo
gremlin.sh 		- symbolic link to gremlin/gremlin.sh
target			- symbolic link to gremlin/target
