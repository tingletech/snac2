#!/bin/env bash
set -eu
which xsltproc
export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" # http://stackoverflow.com/questions/59895
export HOST=`hostname`

# create tomcat config for each server

xslt="$DIR/xslt"

: ${START_LISTEN:="8080"}
: ${START_SHUTDOWN:="12005"}

offset=0
xsltproc \
  -o $DIR/tomcat_xtf/conf/server.xml \
  --stringparam shutdown_string shutdown-this \
  --stringparam shutdown_port $(($START_SHUTDOWN + $offset)) \
  --stringparam listen_port $(($START_LISTEN + $offset))\
  $xslt/generate_config.xslt \
  $xslt/server.xml 

offset=1
xsltproc \
  -o $DIR/tomcat_tinkerpop/conf/server.xml \
  --stringparam shutdown_string shutdown-pop \
  --stringparam shutdown_port $(($START_SHUTDOWN + $offset)) \
  --stringparam listen_port $(($START_LISTEN + $offset))\
  $xslt/generate_config.xslt \
  $xslt/server.xml 

offset=2
xsltproc \
  -o $DIR/tomcat_rdf/conf/server.xml \
  --stringparam shutdown_string shutdown-rdf \
  --stringparam shutdown_port $(($START_SHUTDOWN + $offset)) \
  --stringparam listen_port $(($START_LISTEN + $offset))\
  $xslt/generate_config.xslt \
  $xslt/server.xml

cd $DIR

# generate monit config file
perl -p -e 's/\$\{([^}]+)\}/defined $ENV{$1} ? $ENV{$1} : $&/eg' monitrc.template > monitrc
chmod g-r,o-r monitrc

# create tomcat directories

for confdir in tomcat_xtf tomcat_tinkerpop tomcat_rdf
  do 
    mkdir -p $confdir/logs
    mkdir -p $confdir/work
    mkdir -p $confdir/temp
  done

# create monit directory
mkdir -p $DIR/logs

