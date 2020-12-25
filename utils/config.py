import os
import json

env = os.getenv("ENV")
env_name = env if env else 'development'
with open(f'./configs/{env_name}.json') as json_data_file:
    data = json.load(json_data_file)
print("Load config env=", env_name)

def get_system_config():
    return data

class DeviceType:
    ios = "ios"
    android="android"