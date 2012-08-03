eac-load-graph
==============

Build process for SNAC website.

Setup Environment to build, index, and operate
----------------------------------------------

```
. setenv.bash
```

Make site in a brand new checked out directory
----------------------------------------------

```
export EAC_DIR=/data/production/data			# merge EAC output
export EAC_RAW_DIR=/data/production/data-extract	# merge EAC input
./make.bash
```

Study this script to see how SNAC is built.  It runs other scripts which check out all code, build
all indexes, and configures the tomcat servers.

Requirements

 * bash in $PATH
 * java (tested in java7) in $PATH
 * tomcat (tested in tomcat7) at ~/java/tomcat7
 * maven (mvn) in $PATH
 * mercurial (hg) in $PATH
 * git in $PATH
 * monit in $PATH
 * apache 2.2

Use monit to stop and start
---------------------------

```
./monit				# run with no arguments to start monit daemon
./monit start tomcat_xtf
./monit start tomcat_tinkerpop
./monit start tomcat_rdf
```


Apache Setup
------------

```Include servers/httpd.conf ``` into your main httpd.conf to set up rewrite
rules


License
-------

for code: (e.g. pull_gremlin.bash, load/load_ead.grm, load/load_graphml.grm)
	BSD, see LICENSE-CODE.txt

for the graph as a Database qua Database:
	see the LICENSE-DATA.txt that is distrubuted with the graphML file
	probably one of these http://www.opendatacommons.org/licenses/
