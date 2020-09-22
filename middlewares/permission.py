from functools import wraps
import grpc

def auth_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        context = args[2]
        for key, value in context.invocation_metadata():
            if key == 'accesstoken':
                return f(*args, **kwargs)
        context.set_details("no token provider")
        context.set_code(grpc.StatusCode.UNAUTHENTICATED)
        return
    return wrap