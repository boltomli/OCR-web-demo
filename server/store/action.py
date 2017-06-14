import os
from py2neo import Graph
from . import model

# The db server and u/p should be stored as environment variables
URL = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
U = os.environ.get('NEO4J_USERNAME', 'neo4j')
P = os.environ.get('NEO4J_PASSWORD', '111111')
GRAPH = Graph(url=URL, user=U, password=P)

def get_attempts():
    '''Get a list of all OCR attempts.'''
    return GRAPH.data("MATCH (attempt:Attempt) RETURN attempt")

def get_attempt_by_url(url):
    '''Get one OCR attempt by URL.'''
    return model.Attempt.select(GRAPH, url).first().__ogm__.node
