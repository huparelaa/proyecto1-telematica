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

    

def send_files_to_datanode(data_node_address, route):
    partitions_directory = "splits/uploads"
    if not os.path.exists(partitions_directory):
        print("No partitions to send")
        return

    file_name = route.split("/")[-2]
        
    partitions = sorted(os.listdir(partitions_directory))
    # partition name format: <file_name>-_-part<block_num>
    partitions = [partition for partition in partitions if partition.split("-_-")[0] == file_name]

    for partition in partitions:
        partition_path = os.path.join(partitions_directory, partition)
        with open(partition_path, 'rb') as partition_file:
            content = partition_file.read()
            folder_path = route+partition
            upload_file_with_grpc(folder_path, content, data_node_address)

    delete_splits("uploads")

def download_files_from_datanode(data_node_address, file_name, file_path):
    #remove first "/"
    if file_path[0] == "/":
        file_path = file_path[1:]
    partitions_directory = "splits/downloads"
    if not os.path.exists(partitions_directory):
        os.makedirs(partitions_directory)
    
    # get partition by partition
    block_num = 1
    while True:
        formatted_block_num = f"{block_num:04}"

        response = download_file_with_grpc(f"{file_path}{file_name}/{file_name}{token}{formatted_block_num}", data_node_address)
        if response.content == b'':
            break
        partition_path = os.path.join(partitions_directory, response.name.split("/")[-1])
        
        with open(partition_path, 'wb') as partition_file:
            partition_file.write(response.content)
        block_num += 1
