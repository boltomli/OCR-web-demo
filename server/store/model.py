#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This module provides OGM'''

from py2neo.ogm import GraphObject, Property

class Attempt(GraphObject):
    '''An OCR attempt'''
    __primarykey__ = "filename"
    url = Property()
    caption = Property()
    filename = Property()
