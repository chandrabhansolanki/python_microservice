import grpc
from resume_proto import resume_pb2, resume_pb2_grpc

def client_upload_resume(file_bytes: bytes):
    channel = grpc.insecure_channel('localhost:50052')
    stub = resume_pb2_grpc.ResumeServiceStub(channel)

    response = stub.ParseResume(
        resume_pb2.ResumeRequest(
            file=file_bytes
        )
    )
    return response
