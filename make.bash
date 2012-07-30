#!/usr/bin/env bash
set -eu
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" # http://stackoverflow.com/questions/59895
echo $EAC_DIR
cd $DIR
export GRAPH_JSON=$DIR/snac-graph.json
export GRAPH_GML=$DIR/snac-graph.gml
export GRAPH_ML=$DIR/snac-graphML.xml
export GRAPH_DB=$DIR/snac-neo4j
set -x
./pull_gremlin.bash
./pull_jena-joseki.bash
./pull_rexster.bash
./pull_xtf.bash
./build_graph.bash 
./load_jena.bash 
./index_xtf.bash
./servers/set_ports.bash
