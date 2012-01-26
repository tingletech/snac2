#!/usr/bin/env bash
set -eu
which mvn git
git clone https://github.com/tingletech/jena-joseki
cd jena-joseki
mvn install
cd ..
