import os
import json



def get_system_config():
    env = os.getenv("ENV")
    env_name = env if env else 'development'
    with open(f'./configs/{env_name}.json') as json_data_file:
        data = json.load(json_data_file)
    return data