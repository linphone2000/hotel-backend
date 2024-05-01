from flask import jsonify
from database import database


def get_rooms_by_hotel_id(hotel_id):
    try:
        rooms = list(database.rooms.find({'hotelID': hotel_id}))
        if rooms:
            for room in rooms:
                room['_id'] = str(room['_id'])
            return jsonify(rooms), 200
        else:
            return 'No rooms found for the hotel', 204
    except Exception as e:
        return "Error: "+str(e), 500
