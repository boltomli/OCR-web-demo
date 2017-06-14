from io import BytesIO
import requests
import pytesseract
from wand.image import Image
from PIL import Image as PI
from PIL import ImageFilter

def process_url(url):
    '''OCR image to text'''
    image = Image(blob=BytesIO(requests.get(url).content))
    image_jpeg = process_image(image)
    return pytesseract.image_to_string(image_jpeg)

def process_file(filename):
    '''OCR image to text'''
    image = Image(filename=filename)
    image_jpeg = process_image(image)
    return pytesseract.image_to_string(image_jpeg)

def process_image(image):
    '''Get JPEG image'''
    return PI.open(BytesIO(image.make_blob('jpeg'))).filter(ImageFilter.SHARPEN)
