import os
from dotenv import load_dotenv
from flask_pymongo import pymongo
import googlemaps

load_dotenv()
# CONNECTION_STRING = os.getenv("MONGODB_STRING")
CONNECTION_STRING = os.getenv("MONGODB_STRING_CLOUD")
GOOGLEMAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('gearstalk')
gmaps = googlemaps.Client(key=GOOGLEMAPS_KEY)