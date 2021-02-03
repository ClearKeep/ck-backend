# ref https://pypi.org/project/python-keycloak/

from keycloak import KeycloakOpenID, KeycloakAdmin
from utils.config import get_system_config
import json
# keycloak client
config_keycloak_client = get_system_config()['keycloak_account']
keycloak_openid = KeycloakOpenID(server_url=config_keycloak_client['server_url'],
                                 client_id=config_keycloak_client['client_id'],
                                 realm_name=config_keycloak_client['realm_name'],
                                 client_secret_key=config_keycloak_client['client_secret_key'])
# keycloak admin
config_keycloak_admin = get_system_config()['keycloak_admin']
keycloak_admin = KeycloakAdmin(server_url=config_keycloak_admin['server_url'],
                               username=config_keycloak_admin['username'],
                               password=config_keycloak_admin['password'],
                               realm_name=config_keycloak_admin['realm_name'],
                               client_secret_key=config_keycloak_admin['client_secret_key'],
                               verify=True,
                               auto_refresh_token=['get', 'put', 'post', 'delete'])


class KeyCloakUtils:
    @staticmethod
    def get_well_know(self):
        return keycloak_openid.well_know()

    @staticmethod
    def introspect_token(access_token):
        return keycloak_openid.introspect(access_token)

    @staticmethod
    def get_user_info(access_token):
        return keycloak_openid.userinfo(access_token)

    @staticmethod
    def token(user, password):
        return keycloak_openid.token(user, password)

    @staticmethod
    def refresh_token(user, password):
        return keycloak_openid.refresh_token(user, password)

    @staticmethod
    def create_user(email, password):
        return keycloak_admin.create_user({"email": email,
                                           "username": email,
                                           "enabled": True,
                                           "firstName": "",
                                           "lastName": "",
                                           "credentials": [{"value": password, "type": "password", }]})
    @staticmethod
    def get_user_id_by_email(email):
        return keycloak_admin.get_user_id(email)


    @staticmethod
    def set_user_password(user_id, password):
        return keycloak_admin.set_user_password(user_id=user_id, password=password, temporary=False)

    @staticmethod
    def send_verify_email(user_id):
        return keycloak_admin.send_verify_email(user_id=user_id)

    @staticmethod
    def send_forgot_password(user_id,email):
        return keycloak_admin.send_update_account(
            user_id=user_id,
            payload=json.dumps(['UPDATE_PASSWORD']))
