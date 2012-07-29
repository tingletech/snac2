#!/bin/env bash
set -eu
export PYTHONPATH=~/python-packages/lib/python2.6/site-packages
mkdir -p $PYTHONPATH
easy_install --prefix ~/python-packages rdflib
easy_install --prefix ~/python-packages twill
