import os
import json
import appdirs
from datetime import datetime

APP_NAME = 'mLogger'


def get_config_dir():
    config_dir = appdirs.user_data_dir(APP_NAME)
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def get_config_filename(callsign: str, parkid: str, date: str = None):
    if date is None:
        date = datetime.now().strftime('%Y%m%d')
    return f"{callsign}@{parkid}-{date}.json"


def save_config(callsign: str, parkid: str, config: dict, date: str = None):
    config_dir = get_config_dir()
    filename = get_config_filename(callsign, parkid, date)
    path = os.path.join(config_dir, filename)
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)
    return path


def load_config(callsign: str, parkid: str, date: str = None):
    config_dir = get_config_dir()
    filename = get_config_filename(callsign, parkid, date)
    path = os.path.join(config_dir, filename)
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        return json.load(f)
