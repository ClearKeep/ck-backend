from utils.keycloak import KeyCloakUtils

class AuthService:
    def __init__(self):
        super().__init__()

    def login_user(self, username, password):
        #print("call LoginUser")
        token = KeyCloakUtils.get_token(username, password)
        print(token)
        return token

    def register_user(self, email, username, password):
        #print("call Register User")
        newUserId = KeyCloakUtils.create_user(email, username, password)
        print(newUserId)
        return newUserId  

    #param: name or email
    def get_user_by_name(self, username):
        userId = KeyCloakUtils.get_user_by_username(username)
        print(userId)
        return userId    
