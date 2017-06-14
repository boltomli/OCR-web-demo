from py2neo.ogm import GraphObject, Property

class Attempt(GraphObject):
    '''An OCR attempt'''
    __primarykey__ = "url"
    url = Property()
    caption = Property()
    filename = Property()
