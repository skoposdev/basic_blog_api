import os

import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

def create_token(id: int):
    payload = {
        "id": id,
        "exp": datetime.now() + timedelta(minutes=60),
        "iat": datetime.now(),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_iat": False})
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")