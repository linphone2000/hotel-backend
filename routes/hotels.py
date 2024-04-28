from database import database, save_image_to_gridfs
from bson import ObjectId
from flask import jsonify, request


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


# Post hotel route
def create_hotel():
    try:
        data = request.form
        amenities = data.getlist('amenities')

        # Check hotel already exist
        existing_hotel = database.hotels.find_one({'name': data['name']})
        if existing_hotel:
            return jsonify({'message': "Hotel with the same name already exists"}), 201

        # Saving image to database
        hotel_image = request.files['image']
        hotel_image_id = save_image_to_gridfs(database, hotel_image)

        hotel = {
            'name': data['name'],
            'city': data['city'],
            'image': hotel_image_id,
            'address': data['address'],
            'description': data['description'],
            'rating': data['rating'],
            'checkInTime': data['checkInTime'],
            'checkOutTime': data['checkOutTime'],
            'hotelEmail': data['hotelEmail'],
            'hotelPhone': data['hotelPhone'],
            'amenities': amenities,
            'reviews': []
        }
        # Insert the new hotel into the database
        database.hotels.insert_one(hotel)
        return jsonify({'message': "Hotel created successfully"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
