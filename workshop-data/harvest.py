import rdflib
from rdflib import Namespace, XSD, Literal
from SPARQLWrapper import SPARQLWrapper, JSON

schema = Namespace("http://schema.org/")
dbo = Namespace("http://dbpedia.org/ontology/")
dbr = Namespace("http://dbpedia.org/resource/")
dbpedia = SPARQLWrapper("http://dbpedia.org/sparql")
popQuery = ("""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    SELECT ?country, ?population
    WHERE {
        <%s> dbo:country ?country ;
                dbo:populationTotal ?population .
      }
""")

g = rdflib.Graph()
g.load('workshop-data/swib-past-data.ttl', format="ttl")

for s, p, o in g.triples((None, schema.location, None)):
    if type(o).__name__ == 'URIRef':
        if o.toPython().startswith('http://dbpedia.org'):
            query = popQuery % o.toPython()
            dbpedia.setQuery(query)
            dbpedia.setReturnFormat(JSON)
            results = dbpedia.query().convert()
            for result in results["results"]["bindings"]:
                country = result['country']['value']
                if country:
                    g.add((o, dbo.country, rdflib.URIRef(country)))
                population = result['population']['value']
                if population:
                    g.add((o, dbo.populationTotal, Literal(population, datatype = XSD.nonNegativeInteger)))

g.serialize(destination='workshop-data/swib-past-data.ttl', format='ttl')
