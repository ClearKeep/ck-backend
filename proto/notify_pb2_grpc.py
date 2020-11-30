# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import notify_pb2 as proto_dot_notify__pb2


class NotifyStub(object):
    """Method
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.read_notify = channel.unary_unary(
                '/notification.Notify/read_notify',
                request_serializer=proto_dot_notify__pb2.ReadNotifyRequest.SerializeToString,
                response_deserializer=proto_dot_notify__pb2.BaseResponse.FromString,
                )
        self.get_unread_notifies = channel.unary_unary(
                '/notification.Notify/get_unread_notifies',
                request_serializer=proto_dot_notify__pb2.Empty.SerializeToString,
                response_deserializer=proto_dot_notify__pb2.GetNotifiesResponse.FromString,
                )
        self.subscribe = channel.unary_unary(
                '/notification.Notify/subscribe',
                request_serializer=proto_dot_notify__pb2.SubscribeAndListenRequest.SerializeToString,
                response_deserializer=proto_dot_notify__pb2.BaseResponse.FromString,
                )
        self.listen = channel.unary_stream(
                '/notification.Notify/listen',
                request_serializer=proto_dot_notify__pb2.SubscribeAndListenRequest.SerializeToString,
                response_deserializer=proto_dot_notify__pb2.NotifyObjectResponse.FromString,
                )


class NotifyServicer(object):
    """Method
    """

    def read_notify(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_unread_notifies(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def subscribe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def listen(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NotifyServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'read_notify': grpc.unary_unary_rpc_method_handler(
                    servicer.read_notify,
                    request_deserializer=proto_dot_notify__pb2.ReadNotifyRequest.FromString,
                    response_serializer=proto_dot_notify__pb2.BaseResponse.SerializeToString,
            ),
            'get_unread_notifies': grpc.unary_unary_rpc_method_handler(
                    servicer.get_unread_notifies,
                    request_deserializer=proto_dot_notify__pb2.Empty.FromString,
                    response_serializer=proto_dot_notify__pb2.GetNotifiesResponse.SerializeToString,
            ),
            'subscribe': grpc.unary_unary_rpc_method_handler(
                    servicer.subscribe,
                    request_deserializer=proto_dot_notify__pb2.SubscribeAndListenRequest.FromString,
                    response_serializer=proto_dot_notify__pb2.BaseResponse.SerializeToString,
            ),
            'listen': grpc.unary_stream_rpc_method_handler(
                    servicer.listen,
                    request_deserializer=proto_dot_notify__pb2.SubscribeAndListenRequest.FromString,
                    response_serializer=proto_dot_notify__pb2.NotifyObjectResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'notification.Notify', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Notify(object):
    """Method
    """

    @staticmethod
    def read_notify(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/notification.Notify/read_notify',
            proto_dot_notify__pb2.ReadNotifyRequest.SerializeToString,
            proto_dot_notify__pb2.BaseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_unread_notifies(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/notification.Notify/get_unread_notifies',
            proto_dot_notify__pb2.Empty.SerializeToString,
            proto_dot_notify__pb2.GetNotifiesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def subscribe(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/notification.Notify/subscribe',
            proto_dot_notify__pb2.SubscribeAndListenRequest.SerializeToString,
            proto_dot_notify__pb2.BaseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def listen(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/notification.Notify/listen',
            proto_dot_notify__pb2.SubscribeAndListenRequest.SerializeToString,
            proto_dot_notify__pb2.NotifyObjectResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
