# ref https://pypi.org/project/python-keycloak/
from keycloak import KeycloakOpenID, KeycloakAdmin
from keycloak import raise_error_from_response
from keycloak import KeycloakGetError
from utils.config import get_system_config
import json

URL_ADMIN_REMOVE_USER_SESSIONS = "admin/realms/{realm-name}/users/{id}/logout"
URL_ADMIN_REMOVE_SESSION = "admin/realms/{realm-name}/sessions/{session}"

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
    def refresh_token(refresh_token):
        return keycloak_openid.refresh_token(refresh_token)

    @staticmethod
    def logout(refresh_token):
        keycloak_openid.logout(refresh_token)

    @staticmethod
    def create_user(email, username, password, firstname, lastname):
        return keycloak_admin.create_user({"email": email,
                                           "username": username,
                                           "enabled": True,
                                           "firstName": firstname,
                                           "lastName": lastname,
                                           "credentials": [{"value": password, "type": "password", }]})

    @staticmethod
    def create_user_without_password(email, username, firstname, lastname):
        return keycloak_admin.create_user({"email": email,
                                           "username": username,
                                           "enabled": True,
                                           "firstName": firstname,
                                           "lastName": lastname,
                                           "emailVerified": True
                                           })

    # @staticmethod
    # def create_user_with_username(username, firstname, lastname):
    #     return keycloak_admin.create_user({"email": "",
    #                                        "username": username,
    #                                        "enabled": True,
    #                                        "firstName": firstname,
    #                                        "lastName": lastname,
    #                                        "emailVerified": True
    #                                        })
    #

    @staticmethod
    def get_user_by_email(email):
        try:
            user_id = keycloak_admin.get_user_id(email)
            user = keycloak_admin.get_user(user_id)
            return user
        except Exception as e:
            return None

    @staticmethod
    def set_user_password(user_id, password):
        return keycloak_admin.set_user_password(user_id=user_id, password=password, temporary=False)

    @staticmethod
    def send_verify_email(user_id):
        return keycloak_admin.send_verify_email(user_id=user_id)

    @staticmethod
    def get_sessions(user_id):
        return keycloak_admin.get_sessions(user_id=user_id)

    @staticmethod
    def count_users():
        return keycloak_admin.users_count()

    @staticmethod
    def get_user_id(email):
        return keycloak_admin.get_user_id(email)

    @staticmethod
    def get_clients():
        return keycloak_admin.get_clients()

    @staticmethod
    def delete_user(user_id):
        return keycloak_admin.delete_user(user_id=user_id)

    @staticmethod
    def send_forgot_password(user_id, email):
        return keycloak_admin.send_update_account(
            user_id=user_id,
            payload=json.dumps(['UPDATE_PASSWORD']))

    @staticmethod
    def active_user(user_id):
        return keycloak_admin.update_user(user_id=user_id, payload={'emailVerified': True})

    @staticmethod
    def delete_user(user_id):
        return keycloak_admin.delete_user(user_id=user_id)


    @staticmethod
    def remove_user_sessions(user_id):
        params_path = {
            "realm-name": keycloak_admin.realm_name,
            "id": user_id
        }
        data_raw = keycloak_admin.raw_post(
            URL_ADMIN_REMOVE_USER_SESSIONS.format(**params_path),
            data=None
        )
        return raise_error_from_response(data_raw, KeycloakGetError, expected_codes=[204])

    @staticmethod
    def remove_session(session_id):
        params_path = {
            "realm-name": keycloak_admin.realm_name,
            "session": session_id
        }
        data_raw = keycloak_admin.raw_delete(
            URL_ADMIN_REMOVE_SESSION.format(**params_path),
            data=None
        )
        return raise_error_from_response(data_raw, KeycloakGetError, expected_codes=[204])

if __name__ == "__main__":
    #refresh user
    try:
        token = KeyCloakUtils.token("trungdq1109@gmail.com", "Hello")
        introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
        user_id = introspect_token['sub']
        KeyCloakUtils.delete_user(user_id)
    except:
        pass
    try:
        token = KeyCloakUtils.token("trungdq1@vmodev.com", "NHATle1109")
        introspect_token = KeyCloakUtils.introspect_token(token['access_token'])
        user_id = introspect_token['sub']
        KeyCloakUtils.delete_user(user_id)
    except:
        pass
