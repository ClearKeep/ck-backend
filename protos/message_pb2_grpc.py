# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import message_pb2 as protos_dot_message__pb2


class MessageStub(object):
    """Method
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_messages_in_group = channel.unary_unary(
                '/message.Message/get_messages_in_group',
                request_serializer=protos_dot_message__pb2.GetMessagesInGroupRequest.SerializeToString,
                response_deserializer=protos_dot_message__pb2.GetMessagesInGroupResponse.FromString,
                )
        self.Subscribe = channel.unary_unary(
                '/message.Message/Subscribe',
                request_serializer=protos_dot_message__pb2.SubscribeRequest.SerializeToString,
                response_deserializer=protos_dot_message__pb2.BaseResponse.FromString,
                )
        self.UnSubscribe = channel.unary_unary(
                '/message.Message/UnSubscribe',
                request_serializer=protos_dot_message__pb2.UnSubscribeRequest.SerializeToString,
                response_deserializer=protos_dot_message__pb2.BaseResponse.FromString,
                )
        self.Listen = channel.unary_stream(
                '/message.Message/Listen',
                request_serializer=protos_dot_message__pb2.ListenRequest.SerializeToString,
                response_deserializer=protos_dot_message__pb2.MessageObjectResponse.FromString,
                )
        self.Publish = channel.unary_unary(
                '/message.Message/Publish',
                request_serializer=protos_dot_message__pb2.PublishRequest.SerializeToString,
                response_deserializer=protos_dot_message__pb2.MessageObjectResponse.FromString,
                )
        self.read_messages = channel.unary_unary(
                '/message.Message/read_messages',
                request_serializer=protos_dot_message__pb2.ReadMessagesRequest.SerializeToString,
                response_deserializer=protos_dot_message__pb2.BaseResponse.FromString,
                )
        self.workspace_publish = channel.unary_unary(
                '/message.Message/workspace_publish',
                request_serializer=protos_dot_message__pb2.WorkspacePublishRequest.SerializeToString,
                response_deserializer=protos_dot_message__pb2.MessageObjectResponse.FromString,
                )


class MessageServicer(object):
    """Method
    """

    def get_messages_in_group(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Subscribe(self, request, context):
        """action
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnSubscribe(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Listen(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Publish(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def read_messages(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def workspace_publish(self, request, context):
        """

        rpc edit_message (EditMessageRequest) returns (MessageObjectResponse);
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MessageServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_messages_in_group': grpc.unary_unary_rpc_method_handler(
                    servicer.get_messages_in_group,
                    request_deserializer=protos_dot_message__pb2.GetMessagesInGroupRequest.FromString,
                    response_serializer=protos_dot_message__pb2.GetMessagesInGroupResponse.SerializeToString,
            ),
            'Subscribe': grpc.unary_unary_rpc_method_handler(
                    servicer.Subscribe,
                    request_deserializer=protos_dot_message__pb2.SubscribeRequest.FromString,
                    response_serializer=protos_dot_message__pb2.BaseResponse.SerializeToString,
            ),
            'UnSubscribe': grpc.unary_unary_rpc_method_handler(
                    servicer.UnSubscribe,
                    request_deserializer=protos_dot_message__pb2.UnSubscribeRequest.FromString,
                    response_serializer=protos_dot_message__pb2.BaseResponse.SerializeToString,
            ),
            'Listen': grpc.unary_stream_rpc_method_handler(
                    servicer.Listen,
                    request_deserializer=protos_dot_message__pb2.ListenRequest.FromString,
                    response_serializer=protos_dot_message__pb2.MessageObjectResponse.SerializeToString,
            ),
            'Publish': grpc.unary_unary_rpc_method_handler(
                    servicer.Publish,
                    request_deserializer=protos_dot_message__pb2.PublishRequest.FromString,
                    response_serializer=protos_dot_message__pb2.MessageObjectResponse.SerializeToString,
            ),
            'read_messages': grpc.unary_unary_rpc_method_handler(
                    servicer.read_messages,
                    request_deserializer=protos_dot_message__pb2.ReadMessagesRequest.FromString,
                    response_serializer=protos_dot_message__pb2.BaseResponse.SerializeToString,
            ),
            'workspace_publish': grpc.unary_unary_rpc_method_handler(
                    servicer.workspace_publish,
                    request_deserializer=protos_dot_message__pb2.WorkspacePublishRequest.FromString,
                    response_serializer=protos_dot_message__pb2.MessageObjectResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'message.Message', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Message(object):
    """Method
    """

    @staticmethod
    def get_messages_in_group(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/message.Message/get_messages_in_group',
            protos_dot_message__pb2.GetMessagesInGroupRequest.SerializeToString,
            protos_dot_message__pb2.GetMessagesInGroupResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Subscribe(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/message.Message/Subscribe',
            protos_dot_message__pb2.SubscribeRequest.SerializeToString,
            protos_dot_message__pb2.BaseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UnSubscribe(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/message.Message/UnSubscribe',
            protos_dot_message__pb2.UnSubscribeRequest.SerializeToString,
            protos_dot_message__pb2.BaseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Listen(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/message.Message/Listen',
            protos_dot_message__pb2.ListenRequest.SerializeToString,
            protos_dot_message__pb2.MessageObjectResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Publish(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/message.Message/Publish',
            protos_dot_message__pb2.PublishRequest.SerializeToString,
            protos_dot_message__pb2.MessageObjectResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def read_messages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/message.Message/read_messages',
            protos_dot_message__pb2.ReadMessagesRequest.SerializeToString,
            protos_dot_message__pb2.BaseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def workspace_publish(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/message.Message/workspace_publish',
            protos_dot_message__pb2.WorkspacePublishRequest.SerializeToString,
            protos_dot_message__pb2.MessageObjectResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
