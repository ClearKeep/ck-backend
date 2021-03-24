# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import video_call_pb2 as protos_dot_video__call__pb2


class VideoCallStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.video_call = channel.unary_unary(
                '/video_call.VideoCall/video_call',
                request_serializer=protos_dot_video__call__pb2.VideoCallRequest.SerializeToString,
                response_deserializer=protos_dot_video__call__pb2.ServerResponse.FromString,
                )
        self.cancel_request_call = channel.unary_unary(
                '/video_call.VideoCall/cancel_request_call',
                request_serializer=protos_dot_video__call__pb2.VideoCallRequest.SerializeToString,
                response_deserializer=protos_dot_video__call__pb2.BaseResponse.FromString,
                )
        self.update_call = channel.unary_unary(
                '/video_call.VideoCall/update_call',
                request_serializer=protos_dot_video__call__pb2.UpdateCallRequest.SerializeToString,
                response_deserializer=protos_dot_video__call__pb2.BaseResponse.FromString,
                )


class VideoCallServicer(object):
    """Missing associated documentation comment in .proto file."""

    def video_call(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def cancel_request_call(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update_call(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VideoCallServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'video_call': grpc.unary_unary_rpc_method_handler(
                    servicer.video_call,
                    request_deserializer=protos_dot_video__call__pb2.VideoCallRequest.FromString,
                    response_serializer=protos_dot_video__call__pb2.ServerResponse.SerializeToString,
            ),
            'cancel_request_call': grpc.unary_unary_rpc_method_handler(
                    servicer.cancel_request_call,
                    request_deserializer=protos_dot_video__call__pb2.VideoCallRequest.FromString,
                    response_serializer=protos_dot_video__call__pb2.BaseResponse.SerializeToString,
            ),
            'update_call': grpc.unary_unary_rpc_method_handler(
                    servicer.update_call,
                    request_deserializer=protos_dot_video__call__pb2.UpdateCallRequest.FromString,
                    response_serializer=protos_dot_video__call__pb2.BaseResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'video_call.VideoCall', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class VideoCall(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def video_call(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/video_call.VideoCall/video_call',
            protos_dot_video__call__pb2.VideoCallRequest.SerializeToString,
            protos_dot_video__call__pb2.ServerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def cancel_request_call(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/video_call.VideoCall/cancel_request_call',
            protos_dot_video__call__pb2.VideoCallRequest.SerializeToString,
            protos_dot_video__call__pb2.BaseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update_call(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/video_call.VideoCall/update_call',
            protos_dot_video__call__pb2.UpdateCallRequest.SerializeToString,
            protos_dot_video__call__pb2.BaseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
