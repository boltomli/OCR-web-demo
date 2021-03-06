#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This module provides parsers'''

from flask_restplus import reqparse
from werkzeug.datastructures import FileStorage

IMAGE_URL = reqparse.RequestParser()
IMAGE_URL.add_argument('url',
                       location='form',
                       required=True,
                       help='Image URL')
IMAGE_URL.add_argument('lang',
                       location='form',
                       required=False,
                       help='Language',
                       default='eng')

UPLOAD_FILE = reqparse.RequestParser()
UPLOAD_FILE.add_argument('file',
                         location='files',
                         required=True,
                         type=FileStorage,
                         help='File to upload')
UPLOAD_FILE.add_argument('lang',
                         location='form',
                         required=False,
                         help='Language',
                         default='chi_sim')
