import filetransfer_pb2
import filetransfer_pb2_grpc
import concurrent.futures
import grpc
import sched, time
from services.scheduler import heartBeat
from services.handshake import handShake
import os
from dotenv import load_dotenv
load_dotenv()

class FileTransferServicer(filetransfer_pb2_grpc.FileTransferServicer):
    def UploadFile(self, request, context):
        try:
            partition_token = "-_-part"
            path_components = request.name.split("/")
            base_folder = "./files"

            folder_path = os.path.join(base_folder, *path_components[:-1])
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            file_name_with_partition = path_components[-1]
            file_name = file_name_with_partition.split(partition_token)[0]
            
            file_path = os.path.join(folder_path, file_name_with_partition)
            
            with open(file_path, "wb") as f:
                f.write(request.content)
            
            return filetransfer_pb2.UploadResponse(success=True)
        except Exception as e:
            print(e)
            return filetransfer_pb2.UploadResponse(success=False, message=str(e))

        
    def DownloadFile(self, request, context):
        try:
            file_content = b''
            print(f"Downloading file {request.name}")
            with open(f"./files/{request.name}", 'rb') as f:
                file_content = f.read()
            return filetransfer_pb2.FileChunk(name=request.name, content=file_content)
        except Exception as e:
            print(e)
            return filetransfer_pb2.FileChunk(name=request.name, content=b'')
    
def grpcServer():
    file_size = int(os.getenv("FILE_PART_SIZE"))
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=1),options=[('grpc.max_send_message_length', file_size), ('grpc.max_receive_message_length', file_size)])
    filetransfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferServicer(), server)
    PORT = int(os.environ.get('PORT', 50051))     
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    handShake()
    print(f"Server gRPC started on port {PORT}")
    # my_scheduler = sched.scheduler(time.time, time.sleep)
    # my_scheduler.enter(5, 1, heartBeat, (my_scheduler,))
    # my_scheduler.run()

    server.wait_for_termination()
