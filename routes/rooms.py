from database import database, save_image_to_gridfs
from bson import ObjectId
from flask import request, jsonify


# Get rooms route
def get_rooms():
    try:
        rooms = list(database.rooms.find({}))
        updated_rooms = []
        for room in rooms:
            room['_id'] = str(room['_id'])
            hotelID = room['hotelID']
            hotel = database.hotels.find_one({'_id': ObjectId(hotelID)})
            if hotel:
                room['hotelName'] = hotel['name']
                room['city'] = hotel['city']
            updated_rooms.append(room)
        return jsonify(updated_rooms), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Post room route
def create_room():
    # try:
        data = request.form
        
        # Saving images to database
        roomImage = request.files['image']
        roomImageID = save_image_to_gridfs(database, roomImage)

        new_room = {
            'hotelID': data['hotelID'],
            'roomNumber': data['roomNumber'],
            'roomType': data['roomType'],
            'description': data['description'],
            'maxOccupancy': data['maxOccupancy'],
            'price': data['price'],
            'image': roomImageID,
            'unavailable_dates': []
        }
        # Insert new room into MongoDB
        database.rooms.insert_one(new_room)
        print("Room inserted")
        return jsonify({'message': "Room created successfully"}), 200
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500
