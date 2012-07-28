#!/usr/bin/env bash
set -eu
which mvn git
git clone git@github.com:tingletech/rexster.git
cd rexster
mvn install
cd ..
