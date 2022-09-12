
# ClearKeep  
### Environments
- Python 3  
- Ubuntu/Linux  
 ### Setup require
- PostgreSQL
- Keycloak authentication  
- Janus WebRTC

## 1. Installation  
### 1.1 Install PostgreSQL, Keycloak, Janus WebRTC  
> docker-compose -f .docker/prod-docker-compose.yml up -d  

### 1.2 Using pip3 to install modules  
>pip3 install -r requirement.txt  

## 2. Configuration  
### 2.1 Keycloak authentication  
Setup Keycloak and login as Administrator.

**Realm common setting**
- Use default Master realm or create new realm  
- In General tab: setting value for *Frontend URL* if you want to use custom domain
- In Login tab: switch on *Verify email* and *Login with email*
- In Token tab: enable `Revoke Refresh Token`
- In Email tab: setting SMTP email

**Setting for client:**

In menu Clients, need config for client **admin-cli** and client **account**. Get the config and fill to json config file in project:

For client **admin-cli**:
- In `Settings`:
  - Direct Access Grants Enabled: swicht ON
  - Service Accounts Enabled: switch ON
  - Access Type: select 'confidential'
  - In section `OpenID Connect Compatibility Modes`:
    - Enable `Use Refresh Tokens For Client Credentials Grant`
- In `Service Account Roles`:
  - Assign role `manage-users` to `Client Roles` `realm-management`

Need fill to the configuration file in project:

    "keycloak_admin": {  
          "server_url": "keycloak-server-url",  
          "client_id": "admin-cli",  
          "username": "admin-user-name",  
          "password": "admin-password",  
          "realm_name": "realm-name-1",  
          "client_secret_key": ""  
    }

For client **account**:
- In `Settings`:
  - Direct Access Grants Enabled: switch ON
  - Access Type: select 'confidential'
  - In section `OpenID Connect Compatibility Modes`:
    - Enable `Use Refresh Tokens For Client Credentials Grant`

Need fill to the configuration file in project:

    "keycloak_account": {  
      "server_url": "keycloak-server-url",  
      "client_id": "account",  
      "realm_name": "realm-name-1",  
      "client_secret_key": "secret-key"  
    }

### 2.2 Janus WebRTC  
Need to fill the configuration file in project:

    "janus_webrtc": {  
      "admin_url": "janus-webrtc-admin-url",  
      "client_url" : "janus-webrtc-client-url",  
      "client_ws_url" : "janus-webrtc-client-ws-url",  
      "admin_secret": ""  
    }

Check configuration file of Janus docker in:
 > /usr/local/etc/janus/janus.jcfg

Setting **stun_server** in Nat

Set **admin_secret** and fill to configuration file

Check configuration file of Janus docker in to set path and port:
 > /usr/local/etc/janus/janus.transport.http.jcfg

### 2.3 Other configurations
Project required some configurations, please fill in project config file:

- Aws S3 storage  
- Social login (Facebook, android, office360)
- Firebase push notification
- Stun/turn server
- OTP sender server (currently is twillio)



## 3. Run project  
Genrate protobuf files:
> sh proto/gen.sh

Run project

> python3 app_grpc.py
>
> python3 app_http.py
