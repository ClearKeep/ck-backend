from utils.keycloak import KeyCloakUtils

class AuthService:
    def __init__(self):
        super().__init__()

    def token(self, email, password):
        print("Login User=", email)
        token = KeyCloakUtils.token(email, password)
        return token

    def register_user(self, email, password):
        newUserId = KeyCloakUtils.create_user(email, password)
        print("Register new user ID=", newUserId)
        return newUserId  

    #param: name or email
    def get_user_id_by_email(self, email):
        userId = KeyCloakUtils.get_user_id_by_email(email)
        return userId    
