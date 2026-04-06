from fastapi import APIRouter, HTTPException, Depends
from app.database import users_collection
from app.schemas import UserRegister, UserLogin, GoogleToken
from app.auth import hash_password, verify_password, create_token
from google.oauth2 import id_token
from google.auth.transport import requests
import os
from dotenv import load_dotenv
from app.database import activities_collection
from app.auth import decode_token, oauth2_scheme
from datetime import datetime
from bson import ObjectId

load_dotenv()

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


@router.post("/register")
def register(user: UserRegister):

    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = {

        "account_type": user.account_type,

        "full_name": user.full_name if user.account_type=="individual" else None,

        "organization_name":
            user.organization_name if user.account_type=="organization" else None,

        "phone": user.phone,
        "email": user.email,

        "password": hash_password(user.password),

        "created_at": datetime.utcnow()
    }

    users_collection.insert_one(new_user)

    return {

        "message": "Registered",

        "access_token": create_token({
            "email": user.email
        }),

        "token_type": "bearer"
    }


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
@router.post("/google")
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
    
from fastapi import Depends

@router.get("/activities")

def get_user_activity(

    token: str = Depends(oauth2_scheme)

):

    user_data = decode_token(token)

    data = list(
        activities_collection.find({

            "user_email": user_data["email"]

        }).sort("created_at",-1)
    )

    for d in data:
        d["_id"] = str(d["_id"])

    return data

@router.get("/activity/{id}")

def get_activity(

 id:str,

 token:str = Depends(oauth2_scheme)

):

    user = decode_token(token)

    activity = activities_collection.find_one({

        "_id":ObjectId(id),

        "user_email": user["email"]

    })

    if not activity:

        raise HTTPException(
            status_code=404
        )

    activity["_id"] = str(activity["_id"])

    return activity