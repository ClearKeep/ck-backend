from utils.keycloak import KeyCloakUtils

class AuthService:
    def __init__(self):
        super().__init__()

    def LoginUser(self, username, password):
        print("call LoginUser")
        token = KeyCloakUtils.GetToken(username, password)
        print(token)
        return token

    def RegisterUser(self, email, username, password):
        newUser = KeyCloakUtils.CreateUser(email, username, password)
        print(newUser)
        return newUser    
