from database import database
from bson import json_util

# Get route
def get_data():
    fruits = database.fruits.find()
    formatted_fruits = json_util.dumps(fruits)
    return formatted_fruits, 200
