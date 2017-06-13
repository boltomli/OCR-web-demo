from io import BytesIO
import requests
import pytesseract
from wand.image import Image
from PIL import Image as PI
from PIL import ImageFilter

def process_image(url):
    '''OCR image to text'''
    image = _get_image(url)
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)


def _get_image(url):
    '''Get image from URL'''
    image = Image(blob=BytesIO(requests.get(url).content))
    return PI.open(BytesIO(image.make_blob('jpeg')))
