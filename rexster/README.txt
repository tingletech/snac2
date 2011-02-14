set up rexster

git clone https://github.com/tinkerpop/rexster.git
cd rexster
mvn install

put in the modifed rexster.xml from this directory into 

./target/rexster-0.2-SNAPSHOT/WEB-INF/classes/com/tinkerpop/rexster/rexster.xml

cd target/rexster-0.2-SNAPSHOT
ln -s ../rexster-0.2-SNAPSHOT-standalone/bin/data/ .

then copy or link the neo4j-db file into target/rexster-0.2-SNAPSHOT

in tomcat/webapps; ln -s ...target/rexster-0.2-SNAPSHOT rex
