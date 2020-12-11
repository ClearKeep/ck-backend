from src.controllers.base import ErrorResponse
class Message:
    UNAUTHENTICATED = 1000
    AUTH_USER_NOT_FOUND = 1001
    REGISTER_USER_ALREADY_EXISTS = 1002
    REGISTER_USER_FAILED = 1003
    CHANGE_PASSWORD_FAILED = 1004
    USER_NOT_FOUND = 1005
    GET_PROFILE_FAILED = 1006
    UPDATE_PROFILE_FAILED = 1007
    GET_USER_INFO_FAILED = 1008
    SEARCH_USER_FAILED = 1009
    REGISTER_CLIENT_SIGNAL_KEY_FAILED = 1010
    GET_CLIENT_SIGNAL_KEY_FAILED = 1011
    CLIENT_SIGNAL_KEY_NOT_FOUND = 1012
    CLIENT_PUBLISH_MESSAGE_FAILED = 1013
    CLIENT_SUBCRIBE_FAILED = 1014
    REGISTER_CLIENT_GROUP_KEY_FAILED = 1015
    CREATE_GROUP_CHAT_FAILED = 1016
    GROUP_CHAT_NOT_FOUND = 1017
    GET_GROUP_CHAT_FAILED = 1018
    SEARCH_GROUP_CHAT_FAILED = 1019
    CLIENT_QUEUE_NOT_FOUND = 1020
    #notify
    GET_CLIENT_NOTIFIES_FAILED = 1021
    CLIENT_READ_NOTIFY_FAILED = 1022

    msg_dict = {
        UNAUTHENTICATED: "Authentication required",
        AUTH_USER_NOT_FOUND: "Login information is not correct. Please try again",
        REGISTER_USER_ALREADY_EXISTS: "Username or email is available",
        REGISTER_USER_FAILED: "Register account failed. Please try again",
        CHANGE_PASSWORD_FAILED: "Change password failed. please try again",
        USER_NOT_FOUND: "User information is not correct. Please try again",
        GET_PROFILE_FAILED: "Get profile failed. Please try again",
        UPDATE_PROFILE_FAILED: "Change user profile failed. please try again",
        GET_USER_INFO_FAILED: "Get user information failed. Please try again",
        SEARCH_USER_FAILED: "Search user failed. Please try again",
        REGISTER_CLIENT_SIGNAL_KEY_FAILED: "Register client key failed. Please try again",
        GET_CLIENT_SIGNAL_KEY_FAILED: "Get client key failed. Please try again",
        CLIENT_SIGNAL_KEY_NOT_FOUND: "Client key not found.",
        CLIENT_PUBLISH_MESSAGE_FAILED: "Publish message failed. Please try again",
        CLIENT_SUBCRIBE_FAILED: "Subcribe failed. Please try again",
        REGISTER_CLIENT_GROUP_KEY_FAILED: "Register group key failed. Please try again",
        CREATE_GROUP_CHAT_FAILED: "Create new group failed. Please try again",
        GROUP_CHAT_NOT_FOUND: "Group not found.",
        GET_GROUP_CHAT_FAILED: "Get group failed. Please try again",
        SEARCH_GROUP_CHAT_FAILED: "Search group failed. Please try again",
        CLIENT_QUEUE_NOT_FOUND: "Client queue not found",

        GET_CLIENT_NOTIFIES_FAILED: "Get client notify failed. Please try again",
        CLIENT_READ_NOTIFY_FAILED: "Client read notify failed. Please try again"
    }

    @staticmethod
    def get_message(code):
        return Message.msg_dict[code]

    @staticmethod
    def get_error_object(code):
        return ErrorResponse(code, Message.msg_dict[code])


