import os
import bcrypt
from fastapi import Request
from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timedelta

secret_key = os.getenv("SECRET_KEY")

def get_hashed_password(plain_text_password: str) -> str:
    hashed_password = bcrypt.hashpw(plain_text_password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")

def verify_password(plain_text_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_text_password.encode("utf-8"), hashed_password.encode("utf-8"))

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except JWTError as e:
        raise e
    
def verify_token(req: Request) -> dict:
    try:
        token = req.headers.get("Authorization").split("Bearer ")[1]
        return decode_token(token)
    except JWTError as e:
        raise e

def encode_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm="HS256")

def get_user_id_from_token(token: str) -> int:
    decoded = decode_token(token)
    if decoded:
        return decoded.get("user_id")
    else:
        raise Exception()