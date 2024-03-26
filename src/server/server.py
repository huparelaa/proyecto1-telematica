import grpc
import filetransfer_pb2
import filetransfer_pb2_grpc
import concurrent.futures

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

def server():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=1))
    filetransfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC server started on 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    server()