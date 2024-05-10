from bson import ObjectId
from flask import jsonify, request
from database import database


# Get All Bookings
def get_bookings():
    try:
        updated_bookings = []
        bookings = list(database.bookings.find({}))
        if bookings:
            for booking in bookings:
                hotel = database.hotels.find_one(
                    {'_id': ObjectId(booking['hotelID'])})
                room = database.rooms.find_one(
                    {'_id': ObjectId(booking['roomID'])})
                user = database.users.find_one(
                    {'_id': ObjectId(booking['userID'])})
                updated_booking = {
                    '_id': str(booking['_id']),
                    'userID': booking['userID'],
                    'roomID': booking['roomID'],
                    'hotelID': booking['hotelID'],
                    'stayDates': booking['stayDates'],
                    'totalPrice': booking['totalPrice'],
                    'creationDate': booking['creationDate'],
                    # Additional Hotel Info
                    'hotelName': hotel['name'],
                    'hotelImage': hotel['image'],
                    'hotelAddress': hotel['address'],
                    'hotelRating': hotel['rating'],
                    'hotelCheckIn': hotel['checkInTime'],
                    'hotelCheckOut': hotel['checkOutTime'],
                    'hotelEmail': hotel['hotelEmail'],
                    'hotelPhone': hotel['hotelPhone'],
                    # Additional Room Info
                    'roomNumber': room['roomNumber'],
                    'roomType': room['roomType'],
                    # User info
                    'userEmail': user['email'],
                    'userPhone': user['phone'],
                    'userAddress': user['address'],
                    'userFullName': user['fullName']
                }
                updated_bookings.append(updated_booking)
            updated_bookings.sort(key=lambda x: x['stayDates'][0])
            return jsonify(updated_bookings), 200

        return jsonify(bookings), 200
    except Exception as e:
        return "Error: "+str(e), 500


# Get bookings by user id
def get_bookings_by_user(userID):
    try:
        updated_bookings = []
        bookings = list(database.bookings.find({'userID': userID}))
        if bookings:
            for booking in bookings:
                hotel = database.hotels.find_one(
                    {'_id': ObjectId(booking['hotelID'])})
                room = database.rooms.find_one(
                    {'_id': ObjectId(booking['roomID'])})
                user = database.users.find_one(
                    {'_id': ObjectId(booking['userID'])})
                updated_booking = {
                    '_id': str(booking['_id']),
                    'userID': booking['userID'],
                    'roomID': booking['roomID'],
                    'hotelID': booking['hotelID'],
                    'stayDates': booking['stayDates'],
                    'totalPrice': booking['totalPrice'],
                    'creationDate': booking['creationDate'],
                    # Additional Hotel Info
                    'hotelName': hotel['name'],
                    'hotelImage': hotel['image'],
                    'hotelAddress': hotel['address'],
                    'hotelRating': hotel['rating'],
                    'hotelCheckIn': hotel['checkInTime'],
                    'hotelCheckOut': hotel['checkOutTime'],
                    'hotelEmail': hotel['hotelEmail'],
                    'hotelPhone': hotel['hotelPhone'],
                    # Additional Room Info
                    'roomNumber': room['roomNumber'],
                    'roomType': room['roomType'],
                    # User info
                    'userEmail': user['email'],
                    'userPhone': user['phone'],
                    'userAddress': user['address'],
                    'userFullName': user['fullName']
                }
                updated_bookings.append(updated_booking)
            updated_bookings.sort(key=lambda x: x['stayDates'][0])
            return jsonify(updated_bookings), 200
        else:
            return 'No bookings', 204
    except Exception as e:
        return "Error: "+str(e), 500


# Post Booking
def book():
    try:
        data = request.get_json()

        # Data
        roomID = data.get('roomID')
        unavailableDates = data.get('unavailableDates')
        room_id_obj = ObjectId(roomID)

        # Add unavailable dates to a room
        database.rooms.update_one(
            {"_id": room_id_obj},
            {"$push": {"unavailable_dates": {"$each": unavailableDates}}}
        )

        # Add booking
        database.bookings.insert_one(
            {'userID': data.get('userID'),
             'roomID': data.get('roomID'),
             'hotelID': data.get('hotelID'),
             'stayDates': unavailableDates,
             'totalPrice': data.get('totalPrice'),
             'creationDate': data.get('creationDate')
             }
        )

        return "Success", 200
    except Exception as e:
        return "Error: "+str(e), 500


# Delete Booking
def book_delete(bookingID):
    try:
        booking = database.bookings.find_one({'_id': ObjectId(bookingID)})
        if (booking):
            # Remove unavailable dates from room
            database.rooms.update_one(
                {'_id': ObjectId(booking['roomID']), 'unavailable_dates': {
                    '$in': booking['stayDates']}},
                {'$pull': {'unavailable_dates': {'$in': booking['stayDates']}}}
            )

            # Delete booking
            database.bookings.delete_one({'_id': booking['_id']})

            return "Success", 200
        else:
            return "No booking found!", 204
    except Exception as e:
        return "Error: "+str(e), 500
