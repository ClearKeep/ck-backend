
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

TODO: fix this docs

`docker-compose -f .docker/prod-docker-compose.yml up -d`

### 1.2 Using pip3 to install modules  
```bash
# Use venv to avoid conflict with system-wide python
python3.8 -m venv venv/
# Use venv/bin/python to avoid have to activate the environment
venv/bin/python -m pip install --upgrade pip
venv/bin/python install -r requirements.txt  
```
On Ubuntu 20.04 install these for pip install not to fail
```bash
sudo apt install build-essential libssl-dev libffi-dev libpq-dev  gcc 
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8 python3.8-dev python3.8-venv
venv/bin/python -m pip install wheel
```

## 2. Configuration  
### 2.1 Keycloak authentication  
Setup Keycloak and login as Administrator.

**Realm common setting**
- Use default Master realm or create new realm  
- In General tab: setting value for *Frontend URL* if you want to use custom domain
- In Login tab: switch on *Verify email* and *Login with email*
- In Token tab: setting value for token/refresh_token
- In Email tab: setting SMTP email

**Setting for client:**

In menu Clients, need config for client **admin-cli** and client **account**. Get the config and fill to json config file in project:

For client **admin-cli**:

- Direct Access Grants Enabled: swicht ON
- Service Accounts Enabled: switch ON
- Access Type: select 'confidential'
- In Service account role: assign role for manager user


    "keycloak_admin": {  
          "server_url": "keycloak-server-url",  
          "client_id": "admin-cli",  
          "username": "admin-user-name",  
          "password": "admin-password",  
          "realm_name": "realm-name-1",  
          "client_secret_key": ""  
      }

For client **account**:
- Direct Access Grants Enabled: switch ON
- Access Type: select 'confidential'


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
