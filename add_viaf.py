#!/usr/bin/env python

"""
Adds owl:sameAs links to VIAF using VIAF's autosuggest service. A link
is only put in where there is one unambiguous hit. Mainly just to 
demonstrate the usefulness of using the VIAF identifiers if they are 
known.
"""

import json
import time
import urllib

import rdflib

OWL = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
DCTERMS = rdflib.Namespace("http://purl.org/dc/terms/")


def main():
    g = rdflib.ConjunctiveGraph("Sleepycat")
    try:
        g.open("store")
        for s, o in g.subject_objects(FOAF.name):
            add_viaf(g, s, unicode(o))
            time.sleep(5)
    finally:
        g.close()


def add_viaf(g, s, name):
    hits = viaf(name)
    if hits and len(hits) == 1:
        if hits[0].has_key('viafid'):
            u = "http://viaf.org/viaf/%s/#foaf:Person" % hits[0]['viafid']
            g.add((s, OWL.sameAs, rdflib.URIRef(u)))
            print u


def viaf(q):
    q = q.encode('utf-8')
    url = "http://viaf.org/viaf/AutoSuggest?" + urllib.urlencode({"query": q})
    return json.loads(urllib.urlopen(url).read())["result"]


if __name__ == "__main__":
    main()
