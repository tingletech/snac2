#!/usr/bin/env python

"""
http://inkdroid.org/journal/2011/03/31/snac-hacks/
Ed Summers https://bitbucket.org/edsu
"""

"""
This experimental script will convert the EAC graphml dump to rdf/xml
using rdflib (which you will need to have installed).

    % rdfizer.py graph-snac-example.xml

Which should generate:

    eac.rdf

It uses the FOAF [1] and Arch [2] vocabularies.

[1] http://xmlns.com/foaf/spec/
[2] http://gslis.simmons.edu/archival/arch
"""

import sys
import rdflib

from xml.sax import parse
from xml.sax.handler import ContentHandler

FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
ARCH = rdflib.Namespace("http://purl.org/archival/vocab/arch#")
OWL = rdflib.Namespace("http://www.w3.org/2002/07/owl#")

def main(graphml_file):
    # create rdflib berkeleydb graph to populate
    graph = rdflib.Graph("Sleepycat")
    graph.open("store", create=True)

    # parse the graphml into the graph
    handler = GraphMLHandler(graph)
    parse(graphml_file, handler)

    # output it as turtle and rdf/xml
    graph.bind("arch", ARCH)
    graph.bind("foaf", FOAF)
    graph.serialize(file("eac.rdf", "w"), format="xml")
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
            s = snac_url(n['filename'])
            self.graph.add((s, FOAF.name, rdflib.Literal(n['identity'])))
            if n['entityType'] == 'person':
                self.graph.add((s, rdflib.RDF.type, FOAF.Person))
                # TODO: massage heading into a real name?
                # please don't, we put so much work putting them in inverted order
                # :)
                # don't trust VIAF/dbpedia links for names that are only
                # one word long (no " ") because they are generally dubious
                if " " in n['identity']
                    if "viaf" in n
                        self.graph.add((s, OWL.sameAs, n['viaf']))
                    if "dbpedia" in n
                        self.graph.add((s, OWL.sameAs, n['dbpedia']))
            elif n['entityType'] == 'family':
                self.graph.add((s, rdflib.RDF.type, ARCH.Family))
            elif n['entityType'] == 'corporateBody':
                self.graph.add((s, rdflib.RDF.type, FOAF.Organization))
            # links to collections this person created
            if "creatorOf" in n:
                for u in n['creatorOf'].replace('\n', ' ').split(' '):
                    u = u.strip()
                    if not u:
                        continue
                    u = u + "#Collection"
                    coll = rdflib.URIRef(u)
                    self.graph.add((coll, rdflib.RDF.type, ARCH.Collection))
                    self.graph.add((coll, ARCH.hasProvenance, s))
                    self.graph.add((s, ARCH.primaryProvenanceOf, coll))
            # links to collections this person in mentioned in
            if "associatedWith" in n:
                for u in n['associatedWith'].replace('\n', ' ').split(' '):
                    u = u.strip()
                    if not u:
                        continue
                    u = u + "#Collection"
                    coll = rdflib.URIRef(u)
                    self.graph.add((coll, rdflib.RDF.type, ARCH.Collection))
                    # TODO: does this need a recriprical relationship?
                    # self.graph.add((coll, ARCH.hasProvenance, s))
                    self.graph.add((s, ARCH.referencedIn, coll))
            print self.node['identity']
            self.node = None

        elif name == 'edge':
            s = snac_url(self.edge['from_file'])
            o = snac_url(self.edge['to_file'])
            print "%s -> %s" % (s, o)
            # TODO: make sure these exist?; pretty sure it will
            if self.edge['label'] == 'correspondedWith':
                # make it symmetrical without having to do inferencing
                self.graph.add((s, ARCH['correspondedWith'], o))
                self.graph.add((o, ARCH['correspondedWith'], s))
            elif self.edge['label'] in ['associatedWith', 'associateWith']:
                # done: is this an ok interpretation?
                # yes, checked with @rubinsztajn
                self.graph.add((s, ARCH['appearsWith'], o))
                self.graph.add((o, ARCH['appearsWith'], s))

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
    u = "http://socialarchive.iath.virginia.edu/xtf/view?docId=%s#entity" % name
    return rdflib.URIRef(u)


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
