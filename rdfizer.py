#!/usr/bin/env python

"""
This script will convert the EAC graphml dump to RDF (xml, turtle, ntriples)
using rdflib: 

    % rdfizer.py graph-snac-example.xml

Which should generate:

    eac.rdf
    eac.ttl

It uses the FOAF and Relationship vocabularies, as well as a stub EAC
vocabulary for Family and associatedWith.
"""

import sys
import rdflib

from xml.sax import parse
from xml.sax.handler import ContentHandler

FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
REL = rdflib.Namespace("http://purl.org/vocab/relationship/")
EAC = rdflib.Namespace("http://socialarchive.iath.virginia.edu/ns#")

def main(graphml_file):
    # create rdflib berkeleydb graph to populate
    graph = rdflib.Graph("Sleepycat")
    graph.open("store", create=True)

    # parse the graphml into the graph
    handler = GraphMLHandler(graph)
    parse(graphml_file, handler)

    # output it as turtle and rdf/xml
    graph.bind("rel", REL)
    graph.bind("foaf", FOAF)
    graph.bind("eac", EAC)
    graph.serialize(file("eac.rdf", "w"), format="xml")
    graph.serialize(file("eac.ttl", "w"), format="turtle")
    graph.close()


class GraphMLHandler(ContentHandler):

    def __init__(self, graph):
        self.node = False
        self.edge = False
        self.key = None
        self.graph = graph

    def startElement(self, name, attributes):
        if name == 'node':
            self.node = dict(attributes)
        elif name == 'edge':
            self.edge = dict(attributes)
        elif name == 'data':
            self.key = attributes['key']

    def endElement(self, name):

        if name == 'node':
            n = self.node
            s = snac_url(self.node['identity'])
            if n['entityType'] == 'person':
                self.graph.add((s, rdflib.RDF.type, FOAF.Person))
                self.graph.add((s, FOAF.name, rdflib.Literal(n['identity'])))
            elif n['entityType'] == 'family':
                self.graph.add((s, rdflib.RDF.type, EAC.Family))
                self.graph.add((s, FOAF.name, rdflib.Literal(n['identity'])))
            elif n['entityType'] == 'corporateBody':
                self.graph.add((s, rdflib.RDF.type, FOAF.Organization))
                self.graph.add((s, FOAF.name, rdflib.Literal(n['identity'])))
            if n['urls']:
                for u in n['urls'].replace('\n', ' ').split(' '):
                    self.graph.add((s, FOAF.isPrimaryTopicOf, rdflib.URIRef(u)))
            print self.node['identity']
            self.node = None

        elif name == 'edge':
            s = snac_url(self.edge['from_name'])
            o = snac_url(self.edge['to_name'])
            print "%s -> %s" % (s, o)
            # TODO: make sure these exist?
            if self.edge['label'] == 'correspondedWith':
                self.graph.add((s, REL['collaboratesWith'], o))
            elif self.edge['label'] in ['associatedWith', 'associateWith']:
                # TODO: what does associatedWith mean?
                self.graph.add((s, EAC['associatedWith'], o))

        elif name == 'data':
            self.key = None

    def characters(self, content):
        if not self.key:
            return
        elif self.node:
            self.node[self.key] = self.node.get(self.key, "") + content
        elif self.edge:
            self.edge[self.key] = self.edge.get(self.key, "") + content


def snac_url(name):
    name = name.replace(',', '')
    name = name.replace('.', '')
    name = name.replace(' ', '+')
    u = "http://socialarchive.iath.virginia.edu/xtf/view?docId=%s-cr.xml" % name
    return rdflib.URIRef(u)


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)

