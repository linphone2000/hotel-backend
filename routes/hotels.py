from bson import ObjectId, json_util
from database import database, save_image_to_gridfs
from flask import jsonify, request


# Get hotels route
def get_hotels():
    try:
        hotels = list(database.hotels.find({}))
        updated_hotels = []
        for hotel in hotels:
            # Convert _id to string
            hotel_id = str(hotel['_id'])
            updated_hotel = {
                '_id': hotel_id,
                'name': hotel['name'],
                'city': hotel['city'],
                'image': hotel['image'],
                'address': hotel['address'],
                'description': hotel['description'],
                'rating': hotel['rating'],
                'checkInTime': hotel['checkInTime'],
                'checkOutTime': hotel['checkOutTime'],
                'hotelEmail': hotel['hotelEmail'],
                'hotelPhone': hotel['hotelPhone'],
                'amenities': hotel['amenities'],
                'review': hotel['reviews']
            }
            updated_hotels.append(updated_hotel)
        return jsonify(updated_hotels), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Get hotel by id
def get_hotel_by_hotel_id(hotel_id):
    try:
        hotel_id_obj = ObjectId(hotel_id)
        hotel = database.hotels.find_one({'_id': hotel_id_obj})
        hotel['_id'] = str(hotel['_id'])
        return jsonify(hotel), 200
    except Exception as e:
        return "Error: "+str(e), 500


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


# Edit hotel route
def edit_hotel(hotelID):
    try:
        hotelID = ObjectId(hotelID)
        hotel = database.hotels.find_one({'_id': hotelID})
        if (hotel):
            data = request.form
            updated_hotel = {
                'name': data['name'],
                'city': data['city'],
                'address': data['address'],
                'description': data['description'],
                'rating': data['rating'],
                'checkInTime': data['checkInTime'],
                'checkOutTime': data['checkOutTime'],
                'hotelEmail': data['hotelEmail'],
                'hotelPhone': data['hotelPhone'],
                'amenities': data.getlist('amenities')
            }
            if request.files:
                image = request.files['image']
                imageID = save_image_to_gridfs(database, image)
                updated_hotel['image'] = imageID
            database.hotels.update_one(
                {'_id': hotelID}, {'$set': updated_hotel}
            )
            return "Success", 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Favourite hotel route
def fav_hotel(hotelID):
    try:
        data = request.json
        userID = data['userID']
        result = database.users.update_one(
            {'_id': ObjectId(userID)},
            {'$push': {'favIDs': hotelID}}
        )
        if result.matched_count == 0:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'message': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Favourite hotel remove route
def fav_hotel_remove(hotelID):
    try:
        data = request.json
        userID = data['userID']
        result = database.users.update_one(
            {'_id': ObjectId(userID)},
            {'$pull': {'favIDs': hotelID}}
        )
        if result.matched_count == 0:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'message': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Fetch favourites hotels route
def fetch_favourites():
    try:
        data = request.json
        IDs = (data['favIDs'])
        Object_IDs = [ObjectId(ID) for ID in IDs]

        favHotels = database.hotels.find({'_id': {'$in': Object_IDs}})
        updated_hotels = []

        for hotel in favHotels:
            hotel_id = str(hotel['_id'])
            updated_hotel = {
                '_id': hotel_id,
                'name': hotel['name'],
                'city': hotel['city'],
                'image': hotel['image'],
                'address': hotel['address'],
                'description': hotel['description'],
                'rating': hotel['rating'],
                'checkInTime': hotel['checkInTime'],
                'checkOutTime': hotel['checkOutTime'],
                'hotelEmail': hotel['hotelEmail'],
                'hotelPhone': hotel['hotelPhone'],
                'amenities': hotel['amenities'],
                'review': hotel['reviews']
            }
            updated_hotels.append(updated_hotel)
        return jsonify(updated_hotels), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Delete hotel route
def delete_hotel(hotel_id):
    try:
        # Just for error but unlikely to happen
        hotel = database.hotels.find_one({"_id": ObjectId(hotel_id)})
        if not hotel:
            return jsonify({'error': 'Hotel not found'}), 404

        # Find users with the hotel in their favIDs and remove the hotel ID
        users = database.users.find({"favIDs": hotel_id})
        for user in users:
            if hotel_id in user.get('favIDs', []):
                database.users.update_one(
                    {"_id": user['_id']},
                    {"$pull": {"favIDs": hotel_id}}
                )
                print(
                    f"Removed hotel ID {hotel_id} from user ID {user['_id']}")

        # Delete hotel
        database.hotels.delete_one({"_id": ObjectId(hotel_id)})

        # Delete rooms of that hotel
        database.rooms.delete_many({"hotelID": hotel_id})

        # Delete bookings of that hotel
        database.bookings.delete_many({"hotelID": hotel_id})

        return "success", 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
