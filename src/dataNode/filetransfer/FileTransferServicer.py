import filetransfer_pb2
import filetransfer_pb2_grpc
import os

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
                f.close()
            
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
        

def write_file(file_path, content):
    with open(file_path, "wb") as f:
        f.write(content)