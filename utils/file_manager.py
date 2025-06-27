import json
import os
import yaml
import asyncio

lock = asyncio.Lock()

def load_txt(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass

    else:
        with open(file_path, 'r') as file:
            data = [line.split()[0] for line in file.readlines()]
            return data


def load_json(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as file:
        return json.load(file)
    

def save_session(session_data: list, file_path='data/sessions.json'):
    data = load_json(file_path)
    data[session_data[0]] = session_data[1]
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def load_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return data