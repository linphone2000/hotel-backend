from bson import ObjectId
from flask import send_file
from database import fs


def get_image(image_id):
    try:
        image_data = fs.get(ObjectId(image_id))
        # Adjust mimetype according to your image type
        return send_file(image_data, mimetype='image/jpeg')
    except Exception as e:
        return str(e)
