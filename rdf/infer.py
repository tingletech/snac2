#!/usr/bin/env python

"""
http://inkdroid.org/journal/2011/03/31/snac-hacks/
Ed Summers https://bitbucket.org/edsu
"""

"""
Use the owl:sameAs assertions in the SNAC graph to create a new 
graph oriented around VIAF URIs as subjects and objects.
"""

import rdflib


OWL = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
VIAF = rdflib.URIRef("http://viaf.org")

snac_graph = rdflib.ConjunctiveGraph("Sleepycat")
snac_graph.open("store")

viaf_graph = rdflib.ConjunctiveGraph("Sleepycat", VIAF)
viaf_graph.open("store")

def add(t):
    new_t = []
    for a in t:
        if a.startswith("http://socialarchive.iath.virginia.edu"):
            new_t.append(snac_graph.value(a, OWL.sameAs))
        else:
            new_t.append(a)
    if None not in new_t and new_t[0] != new_t[2]:
        print unicode(new_t).encode("utf-8")
        viaf_graph.add(new_t)


for snac_uri, other_uri in snac_graph.subject_objects(predicate=OWL.sameAs):

    if not snac_uri.startswith("http://socialarchive.iath.virginia.edu"):
        continue

    if not ( other_uri.startswith("http://viaf.org") or other_uri.startswith("http://dbpedia") ):
        continue

    viaf_graph.add((other_uri, OWL.sameAs, snac_uri))

    for s, p, o in snac_graph.triples((snac_uri, None, None)):
        add((other_uri, p, o))

    for s, p, o in snac_graph.triples((None, None, snac_uri)):
        add((s, p, other_uri))


