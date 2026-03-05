from io import BytesIO
import grpc
from resume_proto import resume_pb2_grpc, resume_pb2
from app.utils.utils import extract_text_from_pdf, parse_resume


class ResumeService(resume_pb2_grpc.ResumeServiceServicer):

    def ParseResume(self, request, context):
        try:
            file_bytes = request.file
            file_stream = BytesIO(file_bytes)

            text = extract_text_from_pdf(file_stream)
            parsed_data = parse_resume(text)

            return resume_pb2.ResumeResponse(
                name=parsed_data.get("name", ""),
                email=parsed_data.get("email", ""),
                phone=parsed_data.get("phone", "")
            )

        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))