import os
from pymongo import MongoClient
from dotenv import load_dotenv


# Load .env file
load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(host=MONGO_URI)

API_KEY = os.environ.get('API_KEY')
BASE_URL = "https://api.runway.org.in/v1"

WA_API_KEY = os.environ.get('WA_API_KEY')
WA_API_BASE_URL = "https://wa.runway.org.in/api"
