from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import uuid
from fastapi import Request, HTTPException
from app.core.redis import redis_client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:


    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload["jti"] = str(uuid.uuid4())

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(request: Request):
    token = request.cookies.get('Frontend-user')

    if not token:
        raise HTTPException(status_code=401, detail="Not Authenticated")

    try:
        payload = decode_token(token)
        jti = payload.get("jti")

        if redis_client.exists(f"blacklist:{jti}"):
            raise HTTPException(status_code=401, detail="Token revoked")

        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail={
        "message": "UnAuthorized",
        "status": 401
    })
    except JWTError:
        raise HTTPException(status_code=401,  detail={
        "message": "UnAuthorized",
        "status": 401
    })


