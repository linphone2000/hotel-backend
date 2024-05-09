import base64
from bcrypt import gensalt, hashpw
from bson import ObjectId
from database import database, save_image_to_gridfs
from flask import request, jsonify


# Login route
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Getting the user
    user = database.users.find_one({'email': email})
    if user:
        updatedUser = {
            '_id': str(user['_id']),
            'email': user['email'],
            'fullName': user['fullName'],
            'phone': user['phone'],
            'address': user['address'],
            'image': user['image']
        }

        if user and hashpw(password.encode('utf-8'), user['password']) == user['password']:
            return jsonify({'message': 'Login successful!', 'user': updatedUser}), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 200
    else:
        return jsonify({'message': "User not exists"}), 204


# Register route
def register():
    data = request.form
    email = data.get('email')
    password = data.get('password')
    fullName = data.get('fullName')
    phone = data.get('phone')
    address = data.get('address')
    profileImage = request.files['image']

    # Saving image to database
    profileImageID = save_image_to_gridfs(database, profileImage)

    # Checking for existing user
    existing_user = database.users.find_one({'email': email})
    if existing_user:
        return jsonify({'message': 'User already exists!', "is_registered": False}), 200

    # Password hashing
    hashed_password = hashpw(password.encode('utf-8'), gensalt())

    # User
    new_user = {
        'email': email,
        'password': hashed_password,
        'fullName': fullName,
        'phone': phone,
        'address': address,
        'image': profileImageID
    }

    # Insert data
    database.users.insert_one(new_user)
    return jsonify({'message': "Registration successful.", "is_registered": True}), 200


# User edit route
def edit_user(userID):
    try:
        userID = ObjectId(userID)
        user = database.users.find_one({'_id': userID})
        if (user):
            data = request.form
            updated_user = {
                'fullName': data['fullName'],
                'email': data['email'],
                'phone': data['phone'],
                'address': data['address']
            }
            if request.files:
                image = request.files['image']
                imageID = save_image_to_gridfs(database, image)
                updated_user['image'] = imageID
            database.users.update_one(
                {'_id': userID}, {'$set': updated_user})

            updated_user = get_updated_user(userID)

            updated_user_to_return = {
                '_id': str(updated_user['_id']),
                'email': updated_user['email'],
                'fullName': updated_user['fullName'],
                'phone': updated_user['phone'],
                'address': updated_user['address'],
                'image': updated_user['image']
            }
            print(updated_user_to_return)
            return jsonify({'user': updated_user_to_return}), 200
        else:
            return "No user found!", 204
    except Exception as e:
        return "Error: "+str(e), 500


def get_updated_user(userID):
    return database.users.find_one({'_id': userID})
