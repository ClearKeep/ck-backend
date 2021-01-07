# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos import user_pb2 as protos_dot_user__pb2


class UserStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_profile = channel.unary_unary(
                '/user.User/get_profile',
                request_serializer=protos_dot_user__pb2.Empty.SerializeToString,
                response_deserializer=protos_dot_user__pb2.UserProfileResponse.FromString,
                )
        self.update_profile = channel.unary_unary(
                '/user.User/update_profile',
                request_serializer=protos_dot_user__pb2.UpdateProfileRequest.SerializeToString,
                response_deserializer=protos_dot_user__pb2.BaseResponse.FromString,
                )
        self.change_password = channel.unary_unary(
                '/user.User/change_password',
                request_serializer=protos_dot_user__pb2.ChangePasswordRequest.SerializeToString,
                response_deserializer=protos_dot_user__pb2.BaseResponse.FromString,
                )
        self.get_user_info = channel.unary_unary(
                '/user.User/get_user_info',
                request_serializer=protos_dot_user__pb2.GetUserRequest.SerializeToString,
                response_deserializer=protos_dot_user__pb2.UserInfoResponse.FromString,
                )
        self.search_user = channel.unary_unary(
                '/user.User/search_user',
                request_serializer=protos_dot_user__pb2.SearchUserRequest.SerializeToString,
                response_deserializer=protos_dot_user__pb2.SearchUserResponse.FromString,
                )
        self.get_users = channel.unary_unary(
                '/user.User/get_users',
                request_serializer=protos_dot_user__pb2.Empty.SerializeToString,
                response_deserializer=protos_dot_user__pb2.GetUsersResponse.FromString,
                )


class UserServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_profile(self, request, context):
        """----- FROM MY ACCOUNT -----
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update_profile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def change_password(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_user_info(self, request, context):
        """----- FROM OTHER ACCOUNT -----
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def search_user(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_users(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_UserServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_profile': grpc.unary_unary_rpc_method_handler(
                    servicer.get_profile,
                    request_deserializer=protos_dot_user__pb2.Empty.FromString,
                    response_serializer=protos_dot_user__pb2.UserProfileResponse.SerializeToString,
            ),
            'update_profile': grpc.unary_unary_rpc_method_handler(
                    servicer.update_profile,
                    request_deserializer=protos_dot_user__pb2.UpdateProfileRequest.FromString,
                    response_serializer=protos_dot_user__pb2.BaseResponse.SerializeToString,
            ),
            'change_password': grpc.unary_unary_rpc_method_handler(
                    servicer.change_password,
                    request_deserializer=protos_dot_user__pb2.ChangePasswordRequest.FromString,
                    response_serializer=protos_dot_user__pb2.BaseResponse.SerializeToString,
            ),
            'get_user_info': grpc.unary_unary_rpc_method_handler(
                    servicer.get_user_info,
                    request_deserializer=protos_dot_user__pb2.GetUserRequest.FromString,
                    response_serializer=protos_dot_user__pb2.UserInfoResponse.SerializeToString,
            ),
            'search_user': grpc.unary_unary_rpc_method_handler(
                    servicer.search_user,
                    request_deserializer=protos_dot_user__pb2.SearchUserRequest.FromString,
                    response_serializer=protos_dot_user__pb2.SearchUserResponse.SerializeToString,
            ),
            'get_users': grpc.unary_unary_rpc_method_handler(
                    servicer.get_users,
                    request_deserializer=protos_dot_user__pb2.Empty.FromString,
                    response_serializer=protos_dot_user__pb2.GetUsersResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'user.User', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class User(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get_profile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/user.User/get_profile',
            protos_dot_user__pb2.Empty.SerializeToString,
            protos_dot_user__pb2.UserProfileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update_profile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/user.User/update_profile',
            protos_dot_user__pb2.UpdateProfileRequest.SerializeToString,
            protos_dot_user__pb2.BaseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def change_password(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/user.User/change_password',
            protos_dot_user__pb2.ChangePasswordRequest.SerializeToString,
            protos_dot_user__pb2.BaseResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_user_info(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/user.User/get_user_info',
            protos_dot_user__pb2.GetUserRequest.SerializeToString,
            protos_dot_user__pb2.UserInfoResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def search_user(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/user.User/search_user',
            protos_dot_user__pb2.SearchUserRequest.SerializeToString,
            protos_dot_user__pb2.SearchUserResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_users(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/user.User/get_users',
            protos_dot_user__pb2.Empty.SerializeToString,
            protos_dot_user__pb2.GetUsersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)