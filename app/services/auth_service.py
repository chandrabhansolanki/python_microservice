from app.models.user import User
from app.database import  SessionLocal
from app.auth import create_token, decode_token, verify_password
import grpc

from proto import auth_pb2_grpc, auth_pb2


class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def Login(self, request ,context):
        print("🔥 gRPC LOGIN CALLED 🔥")
        print("Email:", request.email, request.password, 'password')
        db = SessionLocal()
        user = db.query(User).filter(User.email == request.email).first()

        if not user:
            context.abort(
                status_code=grpc.StatusCode.UNAUTHENTICATED,
                details="User not found"
            )

        if not verify_password(request.password, user.hashed_password):
            context.abort(
                status_code=grpc.StatusCode.UNAUTHENTICATED,
                details="Invalid password"
            )

        token = create_token({
            'sub': user.email,
            "role": user.role
        })

        return auth_pb2.LoginResponse(access_token=token, role=user.role, email=user.email)

    def ValidateToken(self, request, context):
        try:
            payload = decode_token(request.token)

            return auth_pb2.UserResponse(
                email=payload["sub"],
                role=payload["role"]
            )

        except Exception:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")