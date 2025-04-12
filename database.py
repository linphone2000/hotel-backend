from werkzeug.utils import secure_filename
import pymongo
from gridfs import GridFS
import certifi


mongo_uri = "mongodb+srv://linphone2000:linphone4321@cluster0.1f5lzka.mongodb.net/mydatabase"
# mongo_uri = "mongodb://localhost:27017/mydatabase"


# database_connect
try:
    client = pymongo.MongoClient(mongo_uri, tlsCAFile=certifi.where())
    # client = pymongo.MongoClient(mongo_uri)
    database = client.get_database()
    fs = GridFS(database)
    print("Connected to MongoDB Atlas successfully!")
except Exception as e:
    print("Connection error:", e)


# file_utils
def save_image_to_gridfs(database, image_file):
    filename = secure_filename(image_file.filename)
    content_type = image_file.content_type

    grid_fs = GridFS(database)
    grid_id = grid_fs.put(
        image_file.read(), filename=filename, content_type=content_type)
    return str(grid_id)
