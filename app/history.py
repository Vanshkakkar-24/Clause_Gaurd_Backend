from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")

db = client["auth_contract_ai"]

history_collection = db["contract_history"]