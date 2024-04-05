import filetransfer_pb2
import filetransfer_pb2_grpc
import grpc

def uploadFileWithGrpc(file_name, file_content, dataNode_address):
    with grpc.insecure_channel(dataNode_address) as channel:  # Connect to the gRPC server
        stub = filetransfer_pb2_grpc.FileTransferStub(channel)
        response = stub.UploadFile(filetransfer_pb2.FileChunk(name=file_name, content=file_content))
        return response.success
    
    