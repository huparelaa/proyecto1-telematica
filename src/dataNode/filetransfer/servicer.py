import filetransfer_pb2_grpc
import concurrent.futures
import grpc
import sched, time
from services.scheduler import heartBeat
from services.handshake import handShake
from filetransfer.FileTransferServicer import FileTransferServicer
import os
from dotenv import load_dotenv
load_dotenv()

def grpcServer():
    file_size = int(os.getenv("FILE_PART_SIZE"))
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=1),options=[('grpc.max_send_message_length', file_size), ('grpc.max_receive_message_length', file_size)])
    filetransfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferServicer(), server)
    PORT = int(os.environ.get('PORT', 50051))     
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    handShake()
    print(f"Server gRPC started on port {PORT}")
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(5, 1, heartBeat, (my_scheduler,))
    my_scheduler.run()

    server.wait_for_termination()
