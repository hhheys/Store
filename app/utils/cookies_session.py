import datetime

import jwt
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response

from app.admin.accessor import get_admin_by_id
from app.config import config
from app.store.database import db

SESSION_DB = {}

COOKIE_NAME = "access_token"

def decode_jwt(token: str):
    try:
        return jwt.decode(token, config.COOKIE_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_admin(request: Request):
    payload = _get_auth_cookie(request)
    if payload and payload["type"]:
        if payload["type"] == "admin":
            try:
                return await get_admin_by_id(payload.get("id"))
            except Exception as e:
                raise HTTPException(status_code=401, detail="Unauthorized")

def send_admin_cookie(response: Response, admin_id: int):
    _send_auth_cookie(response, "admin", admin_id)

def send_user_cookie(response: Response, admin_id: int):
    _send_auth_cookie(response, "user", admin_id)

def _get_auth_cookie(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return decode_jwt(token)

def _send_auth_cookie(response: Response, cookie_type: str, user_id: int):
    payload = {}
    if cookie_type == "user":
        payload = {"type": "user", "id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
    elif cookie_type == "admin":
        payload = {"type": "admin", "id": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
    token = jwt.encode(payload, config.COOKIE_SECRET, algorithm="HS256")
    SESSION_DB[token] = user_id
    print(f"DEBUG: Устанавливаем cookie: {token}")
    response.set_cookie(COOKIE_NAME, token, httponly=True, max_age=3600)