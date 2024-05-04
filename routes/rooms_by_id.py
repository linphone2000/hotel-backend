from bson import ObjectId
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


def get_single_room(room_id):
    try:
        print(type(room_id))
        room_id_obj = ObjectId(room_id)
        room = database.rooms.find_one({'_id': room_id_obj})
        if room is None:
            # Room is still being fetched, respond with a 202 status code (Accepted)
            return "Room data is still being fetched", 202
        room['_id'] = str(room['_id'])
        return jsonify(room), 200
    except Exception as e:
        return "Error: " + str(e), 500
