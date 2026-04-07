from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://vanshkakkar241_db_user:HxyM0T6nxJOwtZuH@clausegaurd.eazlunt.mongodb.net/?appName=ClauseGaurd")

db = client["auth_contract_ai"]

history_collection = db["contract_history"]