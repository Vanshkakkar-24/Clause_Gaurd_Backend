from pymongo import MongoClient

client = MongoClient("mongodb+srv://vanshkakkar241_db_user:HxyM0T6nxJOwtZuH@clausegaurd.eazlunt.mongodb.net/?appName=ClauseGaurd")

db = client["auth_contract_ai"]

users_collection = db["users"]

activities_collection = db["activities"]