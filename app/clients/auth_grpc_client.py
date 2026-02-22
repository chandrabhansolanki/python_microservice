import grpc
from proto import auth_pb2, auth_pb2_grpc

def grpc_login(email, password):
    print("➡️ HTTP → gRPC CALL")
    print("➡️ HTTP → gRPC CALL")

    channel = grpc.insecure_channel("localhost:50051")
    stub = auth_pb2_grpc.AuthServiceStub(channel)

    response = stub.Login(
        auth_pb2.LoginRequest(
            email=email,
            password=password
        )
    )

    return response.access_token, response.role, response.email
