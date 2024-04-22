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
            hotel_id = room['hotel_id']
            hotel = database.hotels.find_one({'_id': ObjectId(hotel_id)})
            if hotel:
                room['hotel_name'] = hotel['name']
                room['city'] = hotel['city']
            updated_rooms.append(room)
        return jsonify(updated_rooms), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Post room route
def create_room():
    try:
        data = request.form

        # Validate input data
        required_fields = ['hotel_name', 'city', 'room_number',
                           'room_type', 'description', 'max_occupancy', 'price']

        if not all(field in data for field in required_fields):
            return jsonify({'missing_fields': True}), 200

        # Check image files
        if 'hotel_image' not in request.files or 'room_image' not in request.files:
            return jsonify({'missing_fields': True, 'type': "image"}), 200

        hotel_image = request.files['hotel_image']
        room_image = request.files['room_image']

        # Saving images to database
        hotel_image_id = save_image_to_gridfs(database, hotel_image)
        room_image_id = save_image_to_gridfs(database, room_image)

        # Check if the hotel exists, or create a new one if it doesn't
        hotel = database.hotels.find_one(
            {'name': data['hotel_name'], 'city': data['city']})
        if not hotel:
            # If the hotel doesn't exist, create a new one
            hotel = {
                'name': data['hotel_name'],
                'city': data['city'],
                'image': hotel_image_id  # Add hotel image
            }
            # Insert the new hotel into the database
            result = database.hotels.insert_one(hotel)
            # Convert ObjectId to string
            hotel['_id'] = str(result.inserted_id)
        else:
            hotel['_id'] = str(hotel['_id'])  # Convert ObjectId to string

        new_room = {
            'hotel_id': hotel['_id'],
            'room_number': data['room_number'],
            'room_type': data['room_type'],
            'description': data['description'],
            'max_occupancy': data['max_occupancy'],
            'price': data['price'],
            'image': room_image_id,  # Add room image
            'unavailable_dates': []
        }
        # Insert new room into MongoDB
        result = database.rooms.insert_one(new_room)

        # Get the inserted room with its ObjectId
        inserted_room = database.rooms.find_one({'_id': result.inserted_id})

        # Convert ObjectId to string
        inserted_room['_id'] = str(inserted_room['_id'])
        inserted_room['hotel'] = hotel

        return jsonify(inserted_room), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
