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
    CLIENT_DECLINE_CALL_FAILED = 1048
    CLIENT_END_CALL_FAILED = 1049
    CLIENT_EDIT_MESSAGE_FAILED = 1050
    ADD_MEMBER_FAILED = 1051
    CREATE_NOTE_FAILED = 1052
    EDIT_NOTE_FAILED = 1053
    DELETE_NOTE_FAILED = 1054
    GET_USER_NOTES_FAILED = 1055

    # add member to group
    ADDER_MEMBER_NOT_IN_GROUP = 1056
    ADDED_USER_IS_ALREADY_MEMBER = 1057
    # leave group
    LEAVED_MEMBER_NOT_IN_GROUP = 1058
    LEAVE_GROUP_FAILED = 1059
    # remove member
    REMOVED_MEMBER_NOT_IN_GROUP = 1060
    REMOVER_MEMBER_NOT_IN_GROUP = 1061
    REMOVE_MEMBER_GROUP_FAILED = 1062
    # leave workspace
    LEAVE_WORKSPACE_FAILED = 1063

    # change status
    UPDATE_USER_STATUS_FAILED = 1047
    PING_PONG_SERVER_FAILED = 1048
    GET_USER_STATUS_FAILED = 1049

    # otp setting
    PHONE_NUMBER_NOT_FOUND = 1050
    NUMBER_OF_ATTEMPTS_OTP_EXCEEDED = 1051
    AUTHEN_SETTING_FLOW_NOT_FOUND = 1052

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
        CLIENT_MISS_CALL_FAILED: "Miss Call failed. Please try again",
        CLIENT_DECLINE_CALL_FAILED: "Decline Call failed. Please try again",
        CLIENT_END_CALL_FAILED: "End Call failed. Please try again",
        ADD_MEMBER_FAILED: "Add Member failed. Please try again",
        CREATE_NOTE_FAILED: "Create Note failed. Please try again",
        EDIT_NOTE_FAILED: "Edit Note failed. Please try again",
        DELETE_NOTE_FAILED: "Delete Note failed. Please try again",
        GET_USER_NOTES_FAILED: "Get User Notes failed. Please try again",

        ADDER_MEMBER_NOT_IN_GROUP: "User is not in the group. Please try again",
        ADDED_USER_IS_ALREADY_MEMBER: "Added user is already a member of the group. \
                Please try again",

        LEAVED_MEMBER_NOT_IN_GROUP: "Leave member is not in group. Please check again",
        LEAVE_GROUP_FAILED: "Leave group failed. Please try again",

        REMOVED_MEMBER_NOT_IN_GROUP: "Removed member is not in group. Please check again",
        REMOVER_MEMBER_NOT_IN_GROUP: "Remover member is not in group. Please check again",
        REMOVE_MEMBER_GROUP_FAILED: "Remover member group failed. Please try again",

        LEAVE_WORKSPACE_FAILED: "Leave Workspace failed. Please try again",

        UPDATE_USER_STATUS_FAILED :"Update status failed. Please try again",
        PING_PONG_SERVER_FAILED :"Ping and pong server failed. Please try again",
        GET_USER_STATUS_FAILED :"Get user status failed. Please try again",

        PHONE_NUMBER_NOT_FOUND: "User must provide phone number to enable this feature.",
        NUMBER_OF_ATTEMPTS_OTP_EXCEEDED: "Exceeded the number of attempts otp. Please wait for 30 minutes and try agains",
        AUTHEN_SETTING_FLOW_NOT_FOUND: "Cannot find current flow of changing otp. Please check the workflow"
    }

    @staticmethod
    def get_message(code):
        return Message.msg_dict[code]

    @staticmethod
    def get_error_object(code):
        return ErrorResponse(code, Message.msg_dict[code])
