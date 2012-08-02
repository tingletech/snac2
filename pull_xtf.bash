#!/usr/bin/env bash
set -eu
which hg ant
hg clone https://code.google.com/p/xtf-cpf/
cd xtf-cpf
hg checkout xtf-cpf
cd WEB-INF
ant
cd ../..
hg clone https://code.google.com/p/xtf-cpf/ xtf-extract
cd xtf-extract
hg checkout xtf-cpf-unmerged
cd WEB-INF
ant
