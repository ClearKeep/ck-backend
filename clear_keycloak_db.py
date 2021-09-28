from utils.keycloak import keycloak_admin

users = [user for user in keycloak_admin.get_users() if user['username'] !='admin']
for user in users:
    keycloak_admin.delete_user(user_id=user['id'])

# token = self.service.token(request.user_id, request.hash_pincode)
#
#
# user_sessions = KeyCloakUtils.get_sessions(user_id=exists_user["id"])
# for user_session in user_sessions:
#     KeyCloakUtils.remove_session(session_id=user_session['id'])
