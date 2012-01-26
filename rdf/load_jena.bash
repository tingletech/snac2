#!/usr/bin/env bash
# http://stackoverflow.com/questions/630372/determine-the-path-of-the-executing-bash-script
MY_PATH="`dirname \"$0\"`"              # relative
MY_PATH="`( cd \"$MY_PATH\" && pwd )`"  # absolutized and normalized
if [ -z "$MY_PATH" ] ; then
  # error; for some reason, the path is not accessible
  # to the script (e.g. permissions re-evaled after suid)
  exit 1  # fail
fi
cd "$MY_PATH"
cd ../jena-joseki/
./bin/tdbload --loc ../eac.tdb ../20110815-graphML+rdf/eac.rdf
./bin/tdbload --loc ../snac-viaf.tdb ../20110815-graphML+rdf/snac-viaf.rdf
