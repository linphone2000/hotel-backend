from bson import ObjectId
from flask import request
from database import database


def book():
    try:
        data = request.get_json()
        roomID = data.get('roomID')
        unavailableDates = data.get('unavailableDates')
        room_id_obj = ObjectId(roomID)
        result = database.rooms.update_one(
            {"_id": room_id_obj},
            {"$push": {"unavailable_dates": {"$each": unavailableDates}}}
        )
        print(result)
        return "Success"
    except Exception as e:
        return "Error: "+str(e), 500
