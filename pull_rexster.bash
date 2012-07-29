#!/usr/bin/env bash
set -eu
which mvn git
git clone https://github.com/tingletech/rexster.git
cd rexster
mvn install
cd ..
cd rexster-extension
mvn install
cd ..
