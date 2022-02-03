import json
from gi.repository import GLib
from ..assets.emoji_list import emojis

# These two helper functions can be used to 
# read and write a json file in the user's configuration directory
#
# If the file does not exits, it will be created

def save_json_config(content: dict or List, filename: str):
    """Saves in a configuration file"""
    config_dir = GLib.get_user_config_dir()
    return GLib.file_set_contents(f"{config_dir}/{filename}.json", json.dumps(content).encode())

def read_json_config(filename: str) -> dict or list or False:
    """Reads from a configuration file"""
    config_dir = GLib.get_user_config_dir()
    config_filename = f"{config_dir}/{filename}.json"

    current_conf_raw = False

    try:
        current_conf_raw = GLib.file_get_contents(config_filename)
    except GLib.Error as e:
        if e.code != GLib.FileError.NOENT:
            return False

    current_conf_json = current_conf_raw.contents.decode() if current_conf_raw else '{}'

    try:
        current_conf = json.loads(current_conf_json)
    except:
        print('Config file is not readable')
        return False

    return current_conf