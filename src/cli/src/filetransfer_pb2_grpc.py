# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import filetransfer_pb2 as filetransfer__pb2


class FileTransferStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UploadFile = channel.unary_unary(
                '/filetransfer.FileTransfer/UploadFile',
                request_serializer=filetransfer__pb2.FileChunk.SerializeToString,
                response_deserializer=filetransfer__pb2.UploadResponse.FromString,
                )
        self.DownloadFile = channel.unary_unary(
                '/filetransfer.FileTransfer/DownloadFile',
                request_serializer=filetransfer__pb2.Request.SerializeToString,
                response_deserializer=filetransfer__pb2.FileChunk.FromString,
                )


class FileTransferServicer(object):
    """Missing associated documentation comment in .proto file."""

    def UploadFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DownloadFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileTransferServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UploadFile': grpc.unary_unary_rpc_method_handler(
                    servicer.UploadFile,
                    request_deserializer=filetransfer__pb2.FileChunk.FromString,
                    response_serializer=filetransfer__pb2.UploadResponse.SerializeToString,
            ),
            'DownloadFile': grpc.unary_unary_rpc_method_handler(
                    servicer.DownloadFile,
                    request_deserializer=filetransfer__pb2.Request.FromString,
                    response_serializer=filetransfer__pb2.FileChunk.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'filetransfer.FileTransfer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FileTransfer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def UploadFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/filetransfer.FileTransfer/UploadFile',
            filetransfer__pb2.FileChunk.SerializeToString,
            filetransfer__pb2.UploadResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DownloadFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/filetransfer.FileTransfer/DownloadFile',
            filetransfer__pb2.Request.SerializeToString,
            filetransfer__pb2.FileChunk.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
