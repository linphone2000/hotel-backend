from bson import ObjectId
from flask import jsonify, request
from database import database, save_image_to_gridfs


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
        room_id_obj = ObjectId(room_id)
        room = database.rooms.find_one({'_id': room_id_obj})
        if room is None:
            # Room is still being fetched, respond with a 202 status code (Accepted)
            return "Room data is still being fetched", 202
        room['_id'] = str(room['_id'])
        return jsonify(room), 200
    except Exception as e:
        return "Error: " + str(e), 500


def edit_room(room_id):
    try:
        print("Edit room route called.")
        roomID = ObjectId(room_id)
        room = database.rooms.find_one({'_id': roomID})
        if (room):
            data = request.form
            print(data)
            updated_room = {
                'roomNumber': data['roomNumber'],
                'roomType': data['roomType'],
                'description': data['description'],
                'maxOccupancy': data['maxOccupancy'],
                'price': data['price']
            }
            if request.files:
                image = request.files['image']
                imageID = save_image_to_gridfs(database, image)
                updated_room['image'] = imageID
            database.rooms.update_one(
                {'_id': roomID}, {'$set': updated_room}
            )
            return "Success", 200
    except Exception as e:
        return "Error: " + str(e), 500


def delete_room(room_id):
    try:
        roomID = ObjectId(room_id)
        room = database.rooms.find_one({'_id': roomID})
        if not room:
            return "Error: room not found", 200
        database.rooms.delete_one({'_id': roomID})
        database.bookings.delete_many({'roomID': room_id})
        return "Success", 200
    except Exception as e:
        return "Error: " + str(e), 500
