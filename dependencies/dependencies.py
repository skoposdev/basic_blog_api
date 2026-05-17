from typing import Annotated

from fastapi import Cookie, HTTPException

from utils.jwt_utils import decode_jwt

async def check_user_auth(token: Annotated[str | None, Cookie()] = None):
    if token is None:
        raise HTTPException(status_code=401, detail="Authentication credentials were not provided")
    try:
        user_jwt = decode_jwt(token)
        return user_jwt
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail=str(e))