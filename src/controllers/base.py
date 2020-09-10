from middlewares.permission import *

class BaseController:
    def __init__(self, service):
        self.service = service