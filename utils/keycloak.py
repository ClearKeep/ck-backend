# ref https://pypi.org/project/python-keycloak/

from keycloak import KeycloakOpenID, KeycloakAdmin
from utils.config import get_system_config

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
                               verify=True)


class KeyCloakUtils:
    @staticmethod
    def get_well_know(self):
        return keycloak_openid.well_know()

    @staticmethod
    def get_token(user, password):
        return keycloak_openid.token(user, password)

    @staticmethod
    def create_user(email, username, password):
        return keycloak_admin.create_user({"email": email,
                                           "username": username,
                                           "enabled": True,
                                           "firstName": "",
                                           "lastName": "",
                                           "credentials": [{"value": password, "type": "password", }]})
    @staticmethod
    def get_user_by_username(username):
        return keycloak_admin.get_user(username)
