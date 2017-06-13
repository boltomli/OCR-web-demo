#! /usr/bin/env python

# -*- coding: utf-8 -*-

from flask import Flask
from flask_restplus import Api, Resource
import parsers, ocr

APP = Flask(__name__)
API = Api(APP, version='1.0', title='OCR API',
          description='Recognize uploaded image or document to text.')
NS = API.namespace('ocr')

@NS.route('/')
@NS.doc(description='OCR')
class Recognize(Resource):
    @NS.expect(parsers.IMAGE_URL)
    def post(self):
        '''Recognize text from image'''
        args = parsers.IMAGE_URL.parse_args()
        return {'ocr': ocr.process_image(args['url'])}

if __name__ == '__main__':
    APP.run(host='0.0.0.0')
