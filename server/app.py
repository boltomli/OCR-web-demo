#! /usr/bin/env python

# -*- coding: utf-8 -*-

import uuid
import datetime
from flask import Flask
from flask_restplus import Api, Resource
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flaskext.couchdb import CouchDBManager, Document, TextField, DateTimeField, ViewField
from werkzeug.utils import secure_filename
import parsers
import ocr

# Settings
DEBUG = False
UPLOADED_ATTEMPTS_DEST = 'upload'
COUCHDB_SERVER = 'http://localhost:5984/'
COUCHDB_DATABASE = 'flask-couchdb'

# Application, RESTful API and namespace
APP = Flask(__name__)
APP.config.from_object(__name__)
API = Api(APP, version='1.0', title='OCR API', doc='/api',
          description='Recognize uploaded image or document to text.')
NS = API.namespace('ocr')

# Uploads

UPLOADED_ATTEMPTS = UploadSet('attempts', IMAGES)
configure_uploads(APP, UPLOADED_ATTEMPTS)

# Database attempts
DBMAN = CouchDBManager()

def unique_id():
    '''Get unique id'''
    return hex(uuid.uuid4().time)[2:-1]

class Attempt(Document):
    '''Each attempt to OCR'''
    doc_type = 'attempt'
    title = TextField()
    filename = TextField()
    caption = TextField()
    published = DateTimeField(default=datetime.datetime.utcnow)

    @property
    def imgsrc(self):
        '''URI for an image'''
        return UPLOADED_ATTEMPTS.url(self.filename)

    all = ViewField('ocrattempt', '''\
        function (doc) {
            if (doc.doc_type == 'attempt')
                emit(doc.published, doc);
        }''', descending=True)

DBMAN.add_document(Attempt)
DBMAN.setup(APP)

# APIs
@NS.route('/')
class ListAttempts(Resource):
    def get(self):
        """Returns list of attempts."""
        attempts = Attempt.all()
        return str(attempts)

@NS.route('/v{}/'.format(API.version))
class Recognize(Resource):
    @API.expect(parsers.IMAGE_URL)
    def post(self):
        '''Recognize text from image'''
        args = parsers.IMAGE_URL.parse_args()
        title = args['url']
        caption = ocr.process_image(args['url'])
        filename = secure_filename(title)
        attempt = Attempt(title=title, caption=caption, filename=filename)
        attempt.id = unique_id()
        attempt.store()
        return {filename: caption}

if __name__ == '__main__':
    APP.run(host='0.0.0.0')
