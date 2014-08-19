#!/usr/bin/env bash
set -eu
which git unzip mvn
wget http://tinkerpop.com/downloads/rexster/rexster-server-2.5.0.zip
unzip rexster-server-2.5.0.zip
ln -s rexster-server-2.5.0 rexster
cd rexster-extension
mvn install
cd ..
