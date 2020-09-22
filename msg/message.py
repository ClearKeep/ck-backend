from src.controllers.base import ErrorResponse
class Message:
    AUTH_USER_NOT_FOUND = 1001
    REGISTER_USER_ALREADY_EXISTS = 1002
    REGISTER_USER_FAILED = 1003

    msg_dict = {
        AUTH_USER_NOT_FOUND: "Login information is not correct. Please try again",
        REGISTER_USER_ALREADY_EXISTS: "Username or email is available",
        REGISTER_USER_FAILED: "Register account failed. Please try again"
    }

    @staticmethod
    def get_message(code):
        return Message.msg_dict[code]

    @staticmethod
    def get_error_object(code):
        return ErrorResponse(code, Message.msg_dict[code])


