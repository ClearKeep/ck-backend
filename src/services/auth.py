from utils.keycloak import KeyCloakUtils

class AuthService:
    def __init__(self):
        super().__init__()

    def token(self, username, password):
        print("Login User=", username)
        token = KeyCloakUtils.token(username, password)
        return token

    def register_user(self, email, username, password):
        newUserId = KeyCloakUtils.create_user(email, username, password)
        print("Register new user ID=", newUserId)
        return newUserId  

    #param: name or email
    def get_user_id_by_username(self, username):
        userId = KeyCloakUtils.get_user_id_by_username(username)
        return userId    
