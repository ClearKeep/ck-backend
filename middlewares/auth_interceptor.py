import grpc

_SIGNATURE_HEADER_KEY = 'authorization'

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
        method_name = handler_call_details.method.split('/')[-1]
        # print("MiddleWare Method Data=", method_name)
        invocation_metadata = handler_call_details.invocation_metadata
        # print("MiddleWare Header Data=", invocation_metadata)
       
        return continuation(handler_call_details)
        # expected_metadata = (_SIGNATURE_HEADER_KEY, method_name[::-1])
        # if expected_metadata in handler_call_details.invocation_metadata:
        #     return continuation(handler_call_details)
        # else:
        #     return self._abortion