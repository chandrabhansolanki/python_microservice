from concurrent import futures
import grpc
from resume_proto import resume_pb2_grpc
from app.services.resume_service import ResumeService




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    resume_pb2_grpc.add_ResumeServiceServicer_to_server(ResumeService(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("Resume gRPC service running on port 50052")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
