# Essentials
from flask import Flask
from flask_cors import CORS
# Routes
from routes.data import get_data
from routes.rooms import get_rooms, create_room
from routes.hotels import get_hotels
from routes.auth import register, login
from routes.image import get_image
from routes.rooms_by_id import get_rooms_by_hotel_id

app = Flask(__name__)
CORS(app)


# Home route
@app.route('/')
def get_data_route():
    return get_data()


# Get image
@app.route('/get_image/<image_id>')
def get_image_route(image_id):
    return get_image(image_id)    


# Rooms route
@app.route('/rooms', methods=['GET'])
def get_rooms_route():
    return get_rooms()


# Route to get hotel by ID
@app.route('/rooms/<hotel_id>', methods=['GET'])
def get_rooms_by_hotel_id_route(hotel_id):
    return get_rooms_by_hotel_id(hotel_id)


# Hotels route
@app.route('/hotels', methods=['GET'])
def get_hotels_route():
    return get_hotels()


# Create room route
@app.route('/rooms', methods=['POST'])
def create_room_route():
    return create_room()


# Register route
@app.route('/register', methods=['POST'])
def register_route():
    return register()


# Login route
@app.route('/login', methods=['POST'])
def login_route():
    return login()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
