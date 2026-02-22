from fastapi import APIRouter, Depends, HTTPException, Response, Request, UploadFile, File
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.database import get_db
from app.models.user import User
from app.auth import hash_password
from app.core.redis import redis_client
from datetime import datetime
from app.auth import get_current_user, decode_token
from app.clients.auth_grpc_client import grpc_login
from app.schemas.user import UserResponse
from typing import List
from PIL import Image
import pytesseract
import io

router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: UserLogin,response: Response):
    try:
        token, role, email = grpc_login(user.email, user.password)

        response.set_cookie(
            key="Frontend-user",
            value=token,
            httponly=True,
        )

        return {"data":{"role": role, "email": email},
                "status": 200}

    except Exception as e:
        print("❌ gRPC ERROR:", e)
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/logout")
def logout(request: Request,response:Response ):
    token = request.cookies.get("Frontend-user")

    if token:
        payload = decode_token(token)
        jti = payload["jti"]
        exp = payload["exp"]

        redis_client.setex(
            name= f"blacklist:{jti}",
            time= exp - int(datetime.utcnow().timestamp()),
            value="true"
        )


    response.delete_cookie(key="Frontend-user", httponly=False, secure=False, samesite="lax")
    return {"message": "User logout successfully", 'status': 200}


@router.get("/userList", response_model=List[UserResponse])
def get_user(user=Depends(get_current_user),db: Session = Depends(get_db)):
    try:
        role = user['role']
        if role == 'admin':
            users = db.query(User).all()
        else:
            users = db.query(User).filter(User.role == role).all()
        return users

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/uploadFile")
async def characterRecognition(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        extracted_text = pytesseract.image_to_string(image)
        return {
            "filename": file.filename,
            "extracted_text": extracted_text
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Image is not readable")


