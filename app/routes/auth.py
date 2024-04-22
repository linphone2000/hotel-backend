from bcrypt import gensalt, hashpw
from database import database
from flask import request, jsonify


# Login route
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Getting the user
    user = database.users.find_one({'username': username})

    if user and hashpw(password.encode('utf-8'), user['password']) == user['password']:
        return jsonify({'message': 'Login successful!', 'user': data.get('username')}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 200


# Register route
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    fullName = data.get('fullName')
    phone = data.get('phone')
    address = data.get('address')

    # Checking for existing user
    existing_user = database.users.find_one({'username': username})
    if existing_user:
        return jsonify({'message': 'User already exists!', "is_registered": False}), 200

    # Password hashing
    hashed_password = hashpw(password.encode('utf-8'), gensalt())

    # Insert data
    database.users.insert_one(
        {'username': username, 'password': hashed_password, 'fullName': fullName, 'phone': phone, 'address': address})
    return jsonify({'message': "Registration successful.", "is_registered": True}), 200