# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import signal_pb2 as protos_dot_signal__pb2


class SignalKeyDistributionStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PeerRegisterClientKey = channel.unary_unary(
                '/signal.SignalKeyDistribution/PeerRegisterClientKey',
                request_serializer=protos_dot_signal__pb2.PeerRegisterClientKeyRequest.SerializeToString,
                response_deserializer=protos_dot_signal__pb2.BaseResponse.FromString,
                )
        self.PeerGetClientKey = channel.unary_unary(
                '/signal.SignalKeyDistribution/PeerGetClientKey',
                request_serializer=protos_dot_signal__pb2.PeerGetClientKeyRequest.SerializeToString,
                response_deserializer=protos_dot_signal__pb2.PeerGetClientKeyResponse.FromString,
                )
        self.GroupRegisterClientKey = channel.unary_unary(
                '/signal.SignalKeyDistribution/GroupRegisterClientKey',
                request_serializer=protos_dot_signal__pb2.GroupRegisterClientKeyRequest.SerializeToString,
                response_deserializer=protos_dot_signal__pb2.BaseResponse.FromString,
                )
        self.GroupUpdateClientKey = channel.unary_unary(
                '/signal.SignalKeyDistribution/GroupUpdateClientKey',
                request_serializer=protos_dot_signal__pb2.GroupUpdateClientKeyRequest.SerializeToString,
                response_deserializer=protos_dot_signal__pb2.BaseResponse.FromString,
                )
        self.GroupGetClientKey = channel.unary_unary(
                '/signal.SignalKeyDistribution/GroupGetClientKey',
                request_serializer=protos_dot_signal__pb2.GroupGetClientKeyRequest.SerializeToString,
                response_deserializer=protos_dot_signal__pb2.GroupGetClientKeyResponse.FromString,
                )
        self.GroupGetAllClientKey = channel.unary_unary(
                '/signal.SignalKeyDistribution/GroupGetAllClientKey',
                request_serializer=protos_dot_signal__pb2.GroupGetAllClientKeyRequest.SerializeToString,
                response_deserializer=protos_dot_signal__pb2.GroupGetAllClientKeyResponse.FromString,
                )
        self.WorkspaceGroupGetClientKey = channel.unary_unary(
                '/signal.SignalKeyDistribution/WorkspaceGroupGetClientKey',
                request_serializer=protos_dot_signal__pb2.WorkspaceGroupGetClientKeyRequest.SerializeToString,
                response_deserializer=protos_dot_signal__pb2.WorkspaceGroupGetClientKeyResponse.FromString,
                )


class SignalKeyDistributionServicer(object):
    """Missing associated documentation comment in .proto file."""

    def PeerRegisterClientKey(self, request, context):
        """peer
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PeerGetClientKey(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GroupRegisterClientKey(self, request, context):
        """group
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GroupUpdateClientKey(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GroupGetClientKey(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GroupGetAllClientKey(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def WorkspaceGroupGetClientKey(self, request, context):
        """workspace
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SignalKeyDistributionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PeerRegisterClientKey': grpc.unary_unary_rpc_method_handler(
                    servicer.PeerRegisterClientKey,
                    request_deserializer=protos_dot_signal__pb2.PeerRegisterClientKeyRequest.FromString,
                    response_serializer=protos_dot_signal__pb2.BaseResponse.SerializeToString,
            ),
            'PeerGetClientKey': grpc.unary_unary_rpc_method_handler(
                    servicer.PeerGetClientKey,
                    request_deserializer=protos_dot_signal__pb2.PeerGetClientKeyRequest.FromString,
                    response_serializer=protos_dot_signal__pb2.PeerGetClientKeyResponse.SerializeToString,
            ),
            'GroupRegisterClientKey': grpc.unary_unary_rpc_method_handler(
                    servicer.GroupRegisterClientKey,
                    request_deserializer=protos_dot_signal__pb2.GroupRegisterClientKeyRequest.FromString,
                    response_serializer=protos_dot_signal__pb2.BaseResponse.SerializeToString,
            ),
            'GroupUpdateClientKey': grpc.unary_unary_rpc_method_handler(
                    servicer.GroupUpdateClientKey,
                    request_deserializer=protos_dot_signal__pb2.GroupUpdateClientKeyRequest.FromString,
                    response_serializer=protos_dot_signal__pb2.BaseResponse.SerializeToString,
            ),
            'GroupGetClientKey': grpc.unary_unary_rpc_method_handler(
                    servicer.GroupGetClientKey,
                    request_deserializer=protos_dot_signal__pb2.GroupGetClientKeyRequest.FromString,
                    response_serializer=protos_dot_signal__pb2.GroupGetClientKeyResponse.SerializeToString,
            ),
            'GroupGetAllClientKey': grpc.unary_unary_rpc_method_handler(
                    servicer.GroupGetAllClientKey,
                    request_deserializer=protos_dot_signal__pb2.GroupGetAllClientKeyRequest.FromString,
                    response_serializer=protos_dot_signal__pb2.GroupGetAllClientKeyResponse.SerializeToString,
            ),
            'WorkspaceGroupGetClientKey': grpc.unary_unary_rpc_method_handler(
                    servicer.WorkspaceGroupGetClientKey,
                    request_deserializer=protos_dot_signal__pb2.WorkspaceGroupGetClientKeyRequest.FromString,
                    response_serializer=protos_dot_signal__pb2.WorkspaceGroupGetClientKeyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'signal.SignalKeyDistribution', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SignalKeyDistribution(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def PeerRegisterClientKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/signal.SignalKeyDistribution/PeerRegisterClientKey',
            protos_dot_signal__pb2.PeerRegisterClientKeyRequest.SerializeToString,
            protos_dot_signal__pb2.BaseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PeerGetClientKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/signal.SignalKeyDistribution/PeerGetClientKey',
            protos_dot_signal__pb2.PeerGetClientKeyRequest.SerializeToString,
            protos_dot_signal__pb2.PeerGetClientKeyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GroupRegisterClientKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/signal.SignalKeyDistribution/GroupRegisterClientKey',
            protos_dot_signal__pb2.GroupRegisterClientKeyRequest.SerializeToString,
            protos_dot_signal__pb2.BaseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GroupUpdateClientKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/signal.SignalKeyDistribution/GroupUpdateClientKey',
            protos_dot_signal__pb2.GroupUpdateClientKeyRequest.SerializeToString,
            protos_dot_signal__pb2.BaseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GroupGetClientKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/signal.SignalKeyDistribution/GroupGetClientKey',
            protos_dot_signal__pb2.GroupGetClientKeyRequest.SerializeToString,
            protos_dot_signal__pb2.GroupGetClientKeyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GroupGetAllClientKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/signal.SignalKeyDistribution/GroupGetAllClientKey',
            protos_dot_signal__pb2.GroupGetAllClientKeyRequest.SerializeToString,
            protos_dot_signal__pb2.GroupGetAllClientKeyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def WorkspaceGroupGetClientKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/signal.SignalKeyDistribution/WorkspaceGroupGetClientKey',
            protos_dot_signal__pb2.WorkspaceGroupGetClientKeyRequest.SerializeToString,
            protos_dot_signal__pb2.WorkspaceGroupGetClientKeyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
