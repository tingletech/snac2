#!/bin/env bash
set -eu
which mvn git
git clone http://github.com/tinkerpop/gremlin.git
cd gremlin
mvn install
cd ..
