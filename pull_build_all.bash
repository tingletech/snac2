#!/usr/bin/env bash
set -eu
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" # http://stackoverflow.com/questions/59895
cd $DIR
set -x
./pull_gremlin.bash
./pull_jena-joseki.bash
./pull_rexster.bash
./pull_xtf.bash
./build_graph.bash 
./load_jena.bash 
./index_xtf.bash 
