#! /usr/bin/env python

# -*- coding: utf-8 -*-

import os
from flask import Flask, send_file
from flask_restplus import Api, Resource
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from werkzeug.utils import secure_filename
import magic
import parsers
import ocr
from store import model, action

# Settings
DEBUG = False
STATIC_PATH = 'static'
UPLOADS_DEFAULT_DEST = '/'.join([STATIC_PATH, 'upload'])
UPLOADS_DEFAULT_URL = UPLOADS_DEFAULT_DEST

# Application, RESTful API and namespace
APP = Flask(__name__, static_folder=STATIC_PATH)
APP.config.from_object(__name__)
API = Api(APP, version='1.0', title='OCR API', doc='/api',
          description='Recognize uploaded image or document to text.')
NS = API.namespace('ocr')

# Uploads

UPLOADED_ATTEMPTS = UploadSet('attempts', IMAGES)
configure_uploads(APP, UPLOADED_ATTEMPTS)
patch_request_class(APP, 32 * 1024 * 1024) # 32M file upload limit

# APIs
@NS.route('/')
class ListAttempts(Resource):
    def get(self):
        """Returns list of attempts."""
        attempts = action.get_attempts()
        return attempts

@NS.route('/retrieve/')
class RetrieveAndRecognize(Resource):
    @API.expect(parsers.IMAGE_URL)
    def post(self):
        '''Recognize text from image URL'''
        args = parsers.IMAGE_URL.parse_args()
        url = args['url']
        attempt = model.Attempt()
        attempt.url = url
        attempt.caption = ocr.process_url(url)
        attempt.filename = secure_filename(url)
        action.GRAPH.push(attempt)
        return action.get_attempt_by_url(url)

@NS.route('/upload/')
class UploadAndRecognize(Resource):
    @API.expect(parsers.UPLOAD_FILE)
    def post(self):
        '''Recognize text from uploaded image'''
        args = parsers.UPLOAD_FILE.parse_args()
        uploaded_file = args['file']
        filename = UPLOADED_ATTEMPTS.save(uploaded_file)
        url = UPLOADED_ATTEMPTS.url(filename)
        attempt = model.Attempt()
        attempt.url = url
        attempt.caption = ocr.process_file(UPLOADED_ATTEMPTS.path(filename))
        attempt.filename = secure_filename(url)
        action.GRAPH.push(attempt)
        return action.get_attempt_by_url(url)

@NS.route('/view/<string:filename>')
class ViewFile(Resource):
    def get(self, filename):
        '''View a file'''
        filepath = os.path.abspath(UPLOADED_ATTEMPTS.path(filename))
        mime = magic.from_file(filepath, mime=True)
        return send_file(filepath, mimetype=mime)

if __name__ == '__main__':
    APP.run(host='0.0.0.0')
