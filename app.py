# Essentials
from flask import Flask
from flask_cors import CORS
# Routes
from routes.data import get_data
from routes.rooms import get_rooms, create_room
from routes.hotels import get_hotels, create_hotel
from routes.auth import edit_user, register, login
from routes.image import get_image
from routes.rooms_by_id import get_rooms_by_hotel_id, get_single_room
from routes.hotels import get_hotel_by_hotel_id
from routes.book import book, book_delete, get_bookings, get_bookings_by_user

app = Flask(__name__)
CORS(app)


# Home route just sample
@app.route('/')
def get_data_route():
    return get_data()


# Get image
@app.route('/get_image/<image_id>')
def get_image_route(image_id):
    return get_image(image_id)


# Hotels
# Crete hotel route
@app.route('/hotels', methods=['POST'])
def create_hotel_route():
    return create_hotel()


# Read Hotels route
@app.route('/hotels', methods=['GET'])
def get_hotels_route():
    return get_hotels()


# Read Hotel by id
@app.route('/hotels/<hotel_id>', methods=['GET'])
def get_hotel_by_id_route(hotel_id):
    return get_hotel_by_hotel_id(hotel_id)


# Read Route to get hotel by ID
@app.route('/rooms/<hotel_id>', methods=['GET'])
def get_rooms_by_hotel_id_route(hotel_id):
    return get_rooms_by_hotel_id(hotel_id)


# Rooms
# Create room route
@app.route('/rooms/', methods=['POST'])
def create_room_route():
    return create_room()


# Read Rooms route
@app.route('/rooms', methods=['GET'])
def get_rooms_route():
    return get_rooms()


# Read single room route
@app.route('/rooms/get_room/<room_id>', methods=['GET'])
def get_single_room_route(room_id):
    return get_single_room(room_id)


# Bookings
# Book route
@app.route('/book', methods=['POST'])
def book_route():
    return book()


# Book delete route
@app.route('/book/<bookingID>', methods=['DELETE'])
def book_delete_route(bookingID):
    return book_delete(bookingID)


# Get bookings route
@app.route('/bookings', methods=['GET'])
def get_bookings_route():
    return get_bookings()


# Get bookings by user route
@app.route('/bookings/<userID>', methods=['GET'])
def get_bookings_by_user_route(userID):
    return get_bookings_by_user(userID)


# Auth
# Register route
@app.route('/register', methods=['POST'])
def register_route():
    return register()


# Login route
@app.route('/login', methods=['POST'])
def login_route():
    return login()


# User edit route
@app.route('/useredit/<userID>', methods=['POST'])
def edit_user_route(userID):
    return edit_user(userID)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
