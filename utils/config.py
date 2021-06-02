import os
import json

env = os.getenv("ENV")
env_name = env if env else 'multiserver'
with open(f'./configs/{env_name}.json') as json_data_file:
    data = json.load(json_data_file)
print("Load config env=", env_name)

def get_system_config():
    return data

def get_system_domain():
    servers = data.get("fd_server")
    for server in servers:
        if server.get('ip_address') == '0.0.0.0':
            return server.get('domain')

def get_ip_domain(domain):
    servers = data.get("fd_server")
    for server in servers:
        if server.get('domain') == domain:
            return server.get('ip_address')
