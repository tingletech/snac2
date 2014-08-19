#!/usr/bin/env bash
set -eu
which git unzip
wget http://tinkerpop.com/downloads/gremlin/gremlin-groovy-2.5.0.zip
unzip gremlin-groovy-2.5.0.zip
ln -s gremlin-groovy-2.5.0 gremlin
