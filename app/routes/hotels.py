from database import database
from bson import ObjectId
from flask import jsonify


# Get hotels route
def get_hotels():
    try:
        hotels = list(database.hotels.find({}))
        updated_hotels = []
        for hotel in hotels:
            # Convert _id to string
            hotel_id = str(hotel['_id'])
            # Fetch rooms associated with the hotel
            # Update hotel details
            updated_hotel = {
                '_id': hotel_id,
                'name': hotel['name'],
                'city': hotel['city'],
                'image': hotel['image'],
            }
            updated_hotels.append(updated_hotel)
        return jsonify(updated_hotels), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
