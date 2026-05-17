from typing import Annotated

from fastapi import APIRouter, HTTPException, Form, Response
from pwdlib import PasswordHash

import database.user_db
from utils.jwt_utils import create_token
from utils.models import UserLogin, UserRegister

router = APIRouter()

@router.post("/auth/login")
async def login_user(res: Response, login: Annotated[UserLogin, Form()]):
    try:
        user = database.user_db.login_user_db(login)
        password_hash = PasswordHash.recommended()
        if password_hash.verify(login.password, user.password):
            token = create_token(user.id)
            res.set_cookie(key="token", value=token, httponly=True)
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/register")
async def register_user(login: Annotated[UserRegister, Form()]):
    try:
        database.user_db.register_user_db(login)
        return {"message": "Register successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/logout")
async def logout_user(res: Response):
    try:
        res.delete_cookie(key="token")
        return {"message": "Logout successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))