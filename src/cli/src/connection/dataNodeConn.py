import grpc
import filetransfer_pb2
import filetransfer_pb2_grpc

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