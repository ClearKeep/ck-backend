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
        KeyCloakUtils.send_verify_email(newUserId)
        print("Register new user ID=", newUserId)
        return newUserId  

    #param: name or email
    def get_user_id_by_email(self, email):
        userId = KeyCloakUtils.get_user_id_by_email(email)
        return userId

    def send_forgot_password(self,email):
        try:
            Userid = self.get_user_id_by_email(email=email)
            if Userid:
                KeyCloakUtils.send_forgot_password(user_id=Userid,email=email)
            return Userid
        except Exception as e:
            raise e

