from concurrent import futures
import grpc
from proto import auth_pb2_grpc
from app.services.auth_service import AuthService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(
        AuthService(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()
    print("Auth gRPC service running on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
