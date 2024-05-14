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
            'image': user['image'],
        }
        if 'favIDs' in user and user['favIDs']:
            updatedUser['favIDs'] = user['favIDs']

        if user and hashpw(password.encode('utf-8'), user['password']) == user['password']:
            return jsonify({'message': 'Login successful!', 'user': updatedUser}), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 200
    else:
        return jsonify({'message': "User not exists"}), 204


# Fetch user route
def fetch_user(userID):
    try:
        user = database.users.find_one({'_id': ObjectId(userID)})
        if user:
            updatedUser = {
                '_id': str(user['_id']),
                'email': user['email'],
                'fullName': user['fullName'],
                'phone': user['phone'],
                'address': user['address'],
                'image': user['image'],
            }
            if 'favIDs' in user and user['favIDs']:
                updatedUser['favIDs'] = user['favIDs']
            return jsonify({'user': updatedUser}), 200
        else:
            return "No user found!", 204
    except Exception as e:
        return "Error: "+str(e), 500


# Admin Login route
def admin_login():
    data = request.form
    print(data)
    email = data.get('email')
    password = data.get('password')

    # Getting the user
    user = database.admins.find_one({'email': email})
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
        'image': "663b3694c914c88056fdf915"
    }

    # Insert data
    database.users.insert_one(new_user)
    return jsonify({'message': "Registration successful.", "is_registered": True}), 200


# Admin Register route
def admin_register():
    data = request.form
    email = data.get('email')
    password = data.get('password')
    fullName = data.get('fullName')
    phone = data.get('phone')
    address = data.get('address')

    # Checking for existing user
    existing_user = database.admins.find_one({'email': email})
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
        'image': "663b3694c914c88056fdf915"
    }

    # Insert data
    database.admins.insert_one(new_user)
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
                'image': updated_user['image'],
            }
            if 'favIDs' in user and user['favIDs']:
                updated_user_to_return['favIDs'] = user['favIDs']
            return jsonify({'user': updated_user_to_return}), 200
        else:
            return "No user found!", 204
    except Exception as e:
        return "Error: "+str(e), 500


# Get all users route
def get_all_users():
    try:
        users = list(database.users.find({}))
        users_to_return = []
        if users:
            for user in users:
                userID = str(user['_id'])
                user_to_return = {
                    '_id': userID,
                    'email': user['email'],
                    'fullName': user['fullName'],
                    'phone': user['phone'],
                    'address': user['address'],
                    'image': user['image']
                }
                users_to_return.append(user_to_return)
            return jsonify(users_to_return), 200
        else:
            return 'No users found for the hotel', 204
    except Exception as e:
        return "Error: "+str(e), 500


def get_updated_user(userID):
    return database.users.find_one({'_id': userID})
