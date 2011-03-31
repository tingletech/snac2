#!/usr/bin/env python

"""
Adds owl:sameAs links to VIAF using the VIAF link found in the HTML
at socialarchive.iath.virginia.edu. This is kind of a hack, considering
the dumped data could include the VIAF URI, but it's just a proof
of concept, so I guess it's bearable. &shrug;
"""

import time
import urllib
import logging

from xml.etree import ElementTree

import rdflib

OWL = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
FOAF = rdflib.Namespace("http://xmlns.com/foaf/0.1/")
DCTERMS = rdflib.Namespace("http://purl.org/dc/terms/")


def main():
    g = rdflib.ConjunctiveGraph("Sleepycat")
    try:
        count = 0
        g.open("store")
        for s in g.subjects(rdflib.RDF.type, FOAF.Person):
            count += 1
            if count <= 4885:
                continue
            viaf_uri = viaf(s)
            if viaf_uri:
                g.add((s, OWL.sameAs, viaf_uri)) 
                logging.info("%s has viaf uri: %s" % (s, viaf_uri))
            time.sleep(1)
    finally:
        g.close()


def viaf(s):
    """scrape viaf uri from snac html
    """
    doc = ElementTree.parse(urllib.urlopen(s.encode("utf-8")))
    for a in doc.findall('.//a'):
        if a.attrib['href'].startswith('http://viaf.org'):
            return rdflib.URIRef("%s/#foaf:Person" % a.attrib['href'])
    logging.warn("unable to lookup viaf URI for %s" % s)
    return None


if __name__ == "__main__":
    logging.basicConfig(filename="add_viaf.log", 
                        format="%(asctime)s - %(levelname)s - %(message)s", 
                        level=logging.INFO)
    main()
