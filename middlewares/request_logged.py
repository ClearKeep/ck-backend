from functools import wraps
from utils.logger import *
import json
import copy

# def request_logged(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         request = args[1]
#         print("Request Object Type=", type(request))
#         print("Request Object=", request)
#         strRequest = json.dumps(request, default=lambda o: o.__dict__)
#         logger.info(strRequest)
#         return
#     return wrap

def request_logged(func):
    def deco(*args, **kwargs):
        # Before request handlers
        print("Request Object Type=", type(args[1]))
        print(args[1])
        # data = json.dumps(args[1], default=lambda o: o.__dict__, sort_keys=True, indent=2)
        # strRequest = json.dumps(args[1])
        rtn = func(*args, **kwargs)
        return rtn
    return deco


class Logger(object):
    def __getattribute__(self, name):
        print('Accessed attribute %s' % name)
        return object.__getattribute__(self, name)
