class BaseController:
    def __init__(self, service):
        self.service = service

class ErrorResponse:
    def __init__(self, code, message):
        self.code = code
        self.message = message