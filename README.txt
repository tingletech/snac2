eac-load-graph
==============

a process to create a directed, attributed, edge-labeled, multi-graph [1] of
social networks derived from processing archival context records [2]

[1] http://engineering.attinteractive.com/2010/12/a-graph-processing-stack/

[2] http://socialarchive.iath.virginia.edu/

Data files
----------

defaults can be changed by setting environmental variables

data 			- EAC_DIR  - symbolic link to EAC files
graph-snac-example.xml	- GRAPH_ML - graphML file
neo4j-db 		- GRAPH_DB - neo4j database created by load_*.grm scripts

Setup Gremlin
-------------

pull_gremlin.bash	
	clone gremlin from github.com/tinkerpop/gremlin and build with mvn

gremlin			- gremlin git repo
gremlin.sh 		- symbolic link to gremlin/gremlin.sh
target			- symbolic link to gremlin/target


Load scripts
------------

./gremlin.sh -e load/load_eac.grm	
	process EAC_DIR and creates GRAPH_ML and GRAPH_DB

./gremlin.sh -e load/load_graphml.grm 	
	process GRAPH_ML and creates GRAPH_DB

License
-------

for code: (e.g. pull_gremlin.bash, load/load_ead.grm, load/load_graphml.grm)
	BSD, see LICENSE-CODE.txt

for the graph as a Database qua Database:
	see the LICENSE-DATA.txt that is distrubuted with the graphML file
	probably one of these http://www.opendatacommons.org/licenses/
