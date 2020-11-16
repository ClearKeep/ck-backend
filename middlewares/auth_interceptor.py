import grpc
from utils.keycloak import KeyCloakUtils


# note: using ServerInterceptor can not access context in service level

class AuthInterceptor(grpc.ServerInterceptor):
    def __init__(self):
        def abort(ignored_request, context):
            context.abort(grpc.StatusCode.UNAUTHENTICATED, 'Invalid authorization')

        self._abortion = grpc.unary_unary_rpc_method_handler(abort)

    def intercept_service(self, continuation, handler_call_details):

        # Example HandlerCallDetails object:
        #     _HandlerCallDetails(
        #       method=u'/helloworld.Greeter/SayHello',
        #       invocation_metadata=...)
        # method_name = handler_call_details.method.split('/')[-1]
        # print("MiddleWare Method Data=", method_name)
        invocation_metadata = handler_call_details.invocation_metadata
        metadata = dict(invocation_metadata)
        # print("MiddleWare Header Data=", invocation_metadata)

        if handler_call_details.method.endswith('login'):
            return continuation(handler_call_details)
        if handler_call_details.method.endswith('register'):
            return continuation(handler_call_details)
        if 'access_token' in metadata and self._token_check(metadata['access_token']):
            return continuation(handler_call_details)
        else:
            return self._abortion

    def _token_check(self, access_token):
        try:
            token_info = KeyCloakUtils.introspect_token(access_token)
            print("auth_interceptor.py => token info here=", token_info)
            if token_info['active']:
                return True
            else:
                return False
        except Exception as e:
            return False

    def _fd_server_check(self, access_token):
        try:
            token_info = KeyCloakUtils.introspect_token(access_token)
            print("auth_interceptor.py => token info here=", token_info)
            if token_info['active']:
                return True
            else:
                return False
        except Exception as e:
            return False
