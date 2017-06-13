from flask_restplus import reqparse

IMAGE_URL = reqparse.RequestParser()
IMAGE_URL.add_argument('url',
                       location='form',
                       required=True,
                       help='Image URL')
