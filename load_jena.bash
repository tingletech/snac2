#!/bin/env bash
# this script processes graphML, creating rdf and SPARQL indexes
set -eux
# need these vars defined
echo $GRAPH_ML
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" # http://stackoverflow.com/questions/59895

rdf_store=$DIR/rdf/store
if [[ -e $rdf_store ]]; then
  read -p "answer y to blow away the old index? " -n 1
  if [[ ! $REPLY =~ ^[Yy]$ ]]
  then
    exit 1
  fi
  rm -rf $rdf_store
fi

cd "$DIR/rdf"

python rdfizer.py $GRAPH_ML
python infer.py
python dump.py

cd "$DIR/jena-joseki/"
./bin/tdbload --loc ../eac.tdb $DIR/rdf/eac.rdf
./bin/tdbload --loc ../snac-viaf.tdb $DIR/rdf/snac-viaf.rdf
