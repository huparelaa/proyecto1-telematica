import filetransfer_pb2
import filetransfer_pb2_grpc
import concurrent.futures
import grpc

import os
from dotenv import load_dotenv
load_dotenv()

class FileTransferServicer(filetransfer_pb2_grpc.FileTransferServicer):
    def UploadFile(self, request, context):
        try:
            folder_path = f"./files/{request.name}"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_path = os.path.join(folder_path, request.name)
            with open(file_path, "wb") as f: 
                f.write(request.content)
            return filetransfer_pb2.UploadResponse(success=True)
        except Exception as e:
            return filetransfer_pb2.UploadResponse(success=False, message=str(e))
        
    def DownloadFile(self, request, context):
        try:
            file_content = b''
            with open(f"./files/{request.name}", 'rb') as f:
                file_content = f.read()
            return filetransfer_pb2.FileChunk(name=request.name, content=file_content)
        except Exception as e:
            return filetransfer_pb2.FileChunk(name=request.name, content=b'')
    
def grpcServer():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=1))
    filetransfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferServicer(), server)
    port = os.getenv("GRPC_PORT")
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server gRPC started on port {port}")
    server.wait_for_termination()
