from database import database
from bson import json_util

# Get route
def get_data():
    hotels = database.hotels.find()
    formatted_hotels = json_util.dumps(hotels)
    return formatted_hotels, 200
