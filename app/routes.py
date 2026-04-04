from fastapi import APIRouter, HTTPException
from app.database import users_collection
from schemas import UserRegister, UserLogin, GoogleToken
from app.auth import hash_password, verify_password, create_token

from google.oauth2 import id_token
from google.auth.transport import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


# ✅ REGISTER
@router.post("/register")
def register(user: UserRegister):

    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    users_collection.insert_one({
        "full_name": user.full_name,
        "phone": user.phone,
        "email": user.email,
        "password": hash_password(user.password)
    })

    return {"message": "User registered successfully"}


# ✅ LOGIN
@router.post("/login")
def login(user: UserLogin):

    query = {"email": user.email} if user.email else {"phone": user.phone}
    db_user = users_collection.find_one(query)

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_token({"email": db_user["email"]})

    return {"access_token": token}


# 🔥 GOOGLE LOGIN
@router.post("/auth/google")
def google_login(data: GoogleToken):

    try:
        idinfo = id_token.verify_oauth2_token(
            data.token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        email = idinfo["email"]
        name = idinfo.get("name", "")

        user = users_collection.find_one({"email": email})

        if not user:
            users_collection.insert_one({
                "full_name": name,
                "email": email,
                "phone": "",
                "password": ""
            })

        token = create_token({"email": email})

        return {"access_token": token}

    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Google token")