#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This module returns OCR result of image from file or URL'''

from io import BytesIO
import requests
import pytesseract as OCR
from wand.image import Image
from PIL import Image as PI
from PIL import ImageFilter as IF

def process_url(url, filename):
    '''OCR image to text'''
    image = Image(blob=BytesIO(requests.get(url).content))
    image.save(filename=filename)
    return process_image(image)

def process_file(filename):
    '''OCR image to text'''
    image = Image(filename=filename)
    return process_image(image)

def process_image(image):
    '''Convert image to sharpened JPEG and OCR'''
    return OCR.image_to_string(PI.open(BytesIO(image.make_blob('jpeg'))).filter(IF.SHARPEN))
