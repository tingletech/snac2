#!/bin/env bash
# this script processes EAC, creating a neo4j db
set -eux
# need these vars defined
echo $GRAPH_DB 
echo $EAC_DIR
echo GRAPH_ML
if [[ -e $GRAPH_DB ]]; then
  read -p "answer y to blow away the old index? " -n 1
  if [[ ! $REPLY =~ ^[Yy]$ ]]
  then
      exit 1
  fi
  rm -r $GRAPH_DB
fi
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" # http://stackoverflow.com/questions/59895
export JAVA_OPTIONS="-Xms32m -Xmx5g"
# create new database
$DIR/gremlin.sh -e $DIR/load/load_eac.grm
