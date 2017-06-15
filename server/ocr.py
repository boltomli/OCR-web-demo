#!/usr/bin/env python

# -*- coding: utf-8 -*-

'''This module returns OCR result of image from file or URL'''

from io import BytesIO
import requests
import pytesseract as OCR
from wand.image import Image
from PIL import Image as PI
from PIL import ImageFilter as IF

def process_url(url, filename, lang):
    '''OCR from URL'''
    with open(filename, 'wb') as f:
        f.write(requests.get(url).content)
    return process_file(filename, lang)

def process_file(filename, lang):
    '''OCR from file'''
    caption = []
    image = Image(filename=filename, resolution=150)
    image_jpeg = image.convert('jpeg')
    for image in image_jpeg.sequence:
        image_page = Image(image=image)
        caption.append(process_image(image_page, lang))
    return ''.join(caption)

def process_image(image, lang='eng'):
    '''Sharpen image and OCR'''
    return OCR.image_to_string(PI.open(BytesIO(image.make_blob('jpeg'))).filter(IF.SHARPEN), lang)
