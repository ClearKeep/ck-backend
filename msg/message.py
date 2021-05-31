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

    # notify
    GET_CLIENT_NOTIFIES_FAILED = 1021
    CLIENT_READ_NOTIFY_FAILED = 1022
    CLIENT_REGISTER_NOTIFY_TOKEN_FAILED = 1023

    # call
    CLIENT_REQUEST_CALL_FAILED = 1025
    # email
    USER_NOT_VERIFY_EMAIL = 1026
    CLIENT_CANCEL_REQUEST_CALL_FAILED = 1027
    CLIENT_UPDATE_CALL_FAILED = 1028

    #google login
    GOOGLE_AUTH_ID_TOKEN_INVALID = 1030
    GOOGLE_AUTH_FAILED = 1031
    # google login
    OFFICE_ACCESS_TOKEN_INVALID = 1032
    OFFICE_AUTH_FAILED = 1033
    # facebook login
    FACEBOOK_ACCESS_TOKEN_INVALID = 1034
    FACEBOOK_AUTH_FAILED = 1035

    #upload file
    UPLOAD_FILE_DATA_LOSS = 1040
    UPLOAD_FILE_FAILED = 1041

    #workspace
    JOIN_WORKSPACE_FAILED = 1045

    EMAIL_ALREADY_USED_FOR_SOCIAL_SIGNIN = 1046
    CLIENT_MISS_CALL_FAILED = 1047
    CLIENT_EDIT_MESSAGE_FAILED = 1050

    msg_dict = {
        UNAUTHENTICATED: "Authentication required",
        AUTH_USER_NOT_FOUND: "Login information is not correct. Please try again",
        REGISTER_USER_ALREADY_EXISTS: "This email address is already being used",
        REGISTER_USER_FAILED: "Register account failed. Please try again",
        USER_NOT_VERIFY_EMAIL: "Your account has not been activated. Please check email for activation link",
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
        CLIENT_READ_NOTIFY_FAILED: "Client read notify failed. Please try again",
        CLIENT_REGISTER_NOTIFY_TOKEN_FAILED: "Client register notification token failed. Please try again",
        CLIENT_REQUEST_CALL_FAILED: "Client request call failed. Please try again",
        CLIENT_CANCEL_REQUEST_CALL_FAILED: "Cancel Request Call failed, Please try again",
        CLIENT_UPDATE_CALL_FAILED: "Update call failed. Please try again",
        GOOGLE_AUTH_ID_TOKEN_INVALID: "Login google failed. Please try again",
        GOOGLE_AUTH_FAILED: "Login google failed. Please try again",
        OFFICE_ACCESS_TOKEN_INVALID: "Login Office 365 failed. Please try again",
        OFFICE_AUTH_FAILED: "Login Office 365 failed. Please try again",
        FACEBOOK_ACCESS_TOKEN_INVALID: "Login Facebook failed. Please try again",
        FACEBOOK_AUTH_FAILED: "Login Facebook failed. Please try again",

        UPLOAD_FILE_DATA_LOSS: "Upload file failed. Data is corrupted",
        UPLOAD_FILE_FAILED: "Upload file failed. Please try again",

        JOIN_WORKSPACE_FAILED: "Join workspace failed. Please try again",
        EMAIL_ALREADY_USED_FOR_SOCIAL_SIGNIN: "The account with this email "
            "does not exist. Please try again",
        CLIENT_EDIT_MESSAGE_FAILED: "Edit message failed. Please try again",
        CLIENT_MISS_CALL_FAILED: "Miss Call failed, Please try again",
    }

    @staticmethod
    def get_message(code):
        return Message.msg_dict[code]

    @staticmethod
    def get_error_object(code):
        return ErrorResponse(code, Message.msg_dict[code])
