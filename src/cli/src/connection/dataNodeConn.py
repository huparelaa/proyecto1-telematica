import grpc
import filetransfer_pb2
import filetransfer_pb2_grpc
from utils.filemanager import delete_splits

import os
token = "-_-part"

def upload_file_with_grpc(file_name, file_content, dataNode_address):
    with grpc.insecure_channel(dataNode_address) as channel:  # Connect to the gRPC server
        stub = filetransfer_pb2_grpc.FileTransferStub(channel)
        response = stub.UploadFile(filetransfer_pb2.FileChunk(name=file_name, content=file_content))
        return response.success

def download_file_with_grpc(file_name, dataNode_address): 
    with grpc.insecure_channel(dataNode_address) as channel: 
        stub = filetransfer_pb2_grpc.FileTransferStub(channel)
        response = stub.DownloadFile(filetransfer_pb2.Request(name=file_name))
        return response
    
def send_file_to_datanode(data_node_address, route, file_name):
    partitions_directory = "splits/uploads"
    if not os.path.exists(partitions_directory):
        print("No partitions to send")
        return
    try:
        partition_path = os.path.join(partitions_directory, file_name)
        with open(partition_path, 'rb') as partition_file:
            content = partition_file.read()
            folder_path = route+file_name
            upload_file_with_grpc(folder_path, content, data_node_address)
    except Exception as e:
        return

def download_file_from_datanode(data_node_address, file_name,file_part, file_path):
    if file_path[0] == "/":
        file_path = file_path[1:]
    partitions_directory = "splits/downloads"
    if not os.path.exists(partitions_directory):
        os.makedirs(partitions_directory)
    try:
        response = download_file_with_grpc(f"{file_path}{file_name}/{file_name}-_-{file_part}", data_node_address)
        partition_path = os.path.join(partitions_directory, response.name.split("/")[-1])
        with open(partition_path, 'wb') as partition_file:
            partition_file.write(response.content)
    except Exception as e:
        return
