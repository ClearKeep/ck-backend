from functools import wraps
from utils.logger import *
import json
import copy


def request_logged(func):
    async def deco(*args, **kwargs):
        # Before request handlers
        print("Request Object Type=", type(args[1]))
        print(args[1])
        # data = json.dumps(args[1], default=lambda o: o.__dict__, sort_keys=True, indent=2)
        # strRequest = json.dumps(args[1])
        return await func(*args, **kwargs)
        # return rtn

    return deco


class Logger(object):
    def __getattribute__(self, name):
        print('Accessed attribute %s' % name)
        return object.__getattribute__(self, name)
