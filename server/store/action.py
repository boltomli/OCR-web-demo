#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This module provides database actions'''

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
    return list(GRAPH.nodes.match('Attempt'))

def get_attempt_by_pk(pk):
    '''Get one OCR attempt by filename.'''
    return GRAPH.nodes.match('Attempt', filename=pk).first()

def save_attempt(url, filename, caption):
    '''Save an attempt'''
    attempt = model.Attempt()
    attempt.url = url
    attempt.filename = filename
    attempt.caption = caption
    GRAPH.push(attempt)
