#!/usr/bin/env python

import rdflib

graph = rdflib.Graph("Sleepycat", rdflib.URIRef("http://viaf.org"))
graph.open("store", create=True)

graph.bind("foaf", rdflib.Namespace("http://xmlns.com/foaf/0.1/"))
graph.bind("arch", rdflib.Namespace("http://purl.org/archival/vocab/arch#"))
graph.bind("owl", rdflib.Namespace("http://www.w3.org/2002/07/owl#"))

graph.serialize(file("snac-viaf.rdf", "w"), format="xml")
graph.close()
