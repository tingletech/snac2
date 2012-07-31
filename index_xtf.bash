#!/bin/env bash
# this script processes EAC, creating a neo4j db
set -eux
# need these vars defined
#read -p "answer y to blow away the old index? " -n 1
#if [[ ! $REPLY =~ ^[Yy]$ ]]
#then
#    exit 1
#fi
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" # http://stackoverflow.com/questions/59895
ln -s $EAC_DIR $DIR/xtf-cpf/data
ln -s $EAC_RAW_DIR $DIR/xtf-extract/data
$DIR/xtf-cpf/bin/textIndexer -index default
$DIR/xtf-extract/bin/textIndexer -index default
