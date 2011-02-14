eac-load-graph
==============

a process to create a directed, attributed, edge-labeled, multi-graph [1]
of social networks derived from processing archival context records [2]

[1] http://engineering.attinteractive.com/2010/12/a-graph-processing-stack/

[2] http://socialarchive.iath.virginia.edu/

Data files
----------

Merged EAC records or a graphML XML file can be used to create the
neo4j database.  

EAC_DIR	- directory of EAC-CPF http://eac.staatsbibliothek-berlin.de/  records
	input to load_eac.grm

GRAPH_ML - a graphML http://graphml.graphdrawing.org/ file
	output from load_eac.grm; input to load_graphml.grm

GRAPH_DB  - neo4j database file
	output from load_eac.grm and load_graphml.grm; input to rexster


Environment Variable Defaults
-----------------------------

defaults are set as if

export EAC_DIR=./data			   
export GRAPH_ML=./graph-snac-example.xml   
export GRAPH_DB=./neo4j-db		   


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
	reads each file in EAC_DIR and creates GRAPH_ML and GRAPH_DB

./gremlin.sh -e load/load_graphml.grm 	
	reads GRAPH_ML and creates GRAPH_DB

Run Gremlin
-----------

./gremlin.sh

         \,,,/
         (o o)
-----oOOo-(_)-oOOo-----
gremlin> g = new Neo4jGraph("neo4j-db")
==>neo4jgraph[EmbeddedGraphDatabase [neo4j-db]]
gremlin> g.V.count()
==>124152
gremlin> g.E.count()
==>245367

gremlin> results = g.idx(T.v)[[identity:'Bush, Vannevar, 1890-1974.']]
==>v[61472]
gremlin> print results                                                     
com.tinkerpop.blueprints.pgm.impls.neo4j.util.Neo4jVertexSequence@76c7cadf==>null

gremlin> results = g.idx(T.v).get("identity", "Bush, Vannevar, 1890-1974.")>>1
==>v[61472]
gremlin> print results
v[61472]==>null

gremlin> results = idx.get("identity", Neo4jTokens.QUERY_HEADER+"Franklin*Ben*")._.identity
==>Franklin, Benjamin, 1706-1790.
==>Franklin, Benjamin.

gremlin> g.shutdown()
==>null
gremlin> exit

x = []
g.v(61472).outE.inV.aggregate(x).outE.inV.except(x).unique._.identity

See also 
	- https://github.com/tinkerpop/gremlin/wiki
	- https://github.com/tinkerpop/gremlin/wiki/Learning-Dependencies

Rexster
-------

see rexster/README.txt

Graph Schema
------------

vertex properties:  
	_id: auto-assigned by neo4j
	_type: vertex
	identity: the name of the entity (string)
	urls: \n seperated list of source EAD files  
        entityType: 'corporateBody', 'family', or 'person'

edge properties:
	_id: auto-assigned by neo4j
	_type: edge
	_lable: 'correspondedWith' or 'associatedWith'
	_inV: incoming vertex (from)
	_outV: outgoing vertex (to)
	from_name: from identity (string) denormalized
	to_name: to identity (string) denormalized

License
-------

for code: (e.g. pull_gremlin.bash, load/load_ead.grm, load/load_graphml.grm)
	BSD, see LICENSE-CODE.txt

for the graph as a Database qua Database:
	see the LICENSE-DATA.txt that is distrubuted with the graphML file
	probably one of these http://www.opendatacommons.org/licenses/
