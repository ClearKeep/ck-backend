from utils.keycloak import keycloak_admin

users = [user for user in keycloak_admin.get_users() if user['username'] !='admin']
for user in users:
    keycloak_admin.delete_user(user_id=user['id'])
