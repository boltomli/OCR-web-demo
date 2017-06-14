#! /usr/bin/env python

# -*- coding: utf-8 -*-

from flask import Flask
from flask_restplus import Api, Resource
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
import parsers
import ocr
from store import model, action

# Settings
DEBUG = False
UPLOADED_ATTEMPTS_DEST = 'upload'

# Application, RESTful API and namespace
APP = Flask(__name__)
APP.config.from_object(__name__)
API = Api(APP, version='1.0', title='OCR API', doc='/api',
          description='Recognize uploaded image or document to text.')
NS = API.namespace('ocr')

# Uploads

UPLOADED_ATTEMPTS = UploadSet('attempts', IMAGES)
configure_uploads(APP, UPLOADED_ATTEMPTS)

# APIs
@NS.route('/')
class ListAttempts(Resource):
    def get(self):
        """Returns list of attempts."""
        attempts = action.get_attempts()
        return attempts

@NS.route('/v{}/'.format(API.version))
class Recognize(Resource):
    @API.expect(parsers.IMAGE_URL)
    def post(self):
        '''Recognize text from image'''
        args = parsers.IMAGE_URL.parse_args()
        url = args['url']
        attempt = model.Attempt()
        attempt.url = url
        attempt.caption = ocr.process_image(url)
        attempt.filename = secure_filename(url)
        action.GRAPH.push(attempt)
        return action.get_attempt_by_url(url)

if __name__ == '__main__':
    APP.run(host='0.0.0.0')
