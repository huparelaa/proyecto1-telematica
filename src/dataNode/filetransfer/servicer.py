import filetransfer_pb2
import filetransfer_pb2_grpc
import concurrent.futures
import grpc
import asyncio
from grpc.experimental import aio

import os
from dotenv import load_dotenv
load_dotenv()

class FileTransferServicer(filetransfer_pb2_grpc.FileTransferServicer):
    def UploadFile(self, request, context):
        with open(f"./files/{request.name}", "wb") as f: 
            f.write(request.content)
        return filetransfer_pb2.UploadResponse(success=True)
    
    def DownloadFile(self, request, context):
        file_content = b''
        with open(f"./files/{request.name}", 'rb') as f:
            file_content = f.read()
        return filetransfer_pb2.FileChunk(name=request.name, content=file_content)
    
async def grpcServer():
    server = aio.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    filetransfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferServicer(), server)
    port = os.getenv("GRPC_PORT")
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    print(f"Server gRPC started on port {port}")
    await server.wait_for_termination()