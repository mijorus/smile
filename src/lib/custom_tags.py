import json
from gi.repository import GLib
from .emoji_list import emojis

def remove_config_file():
    pass

def set_custom_tags(emoji: str, tags: str):
    """Saves the new tags for a given emoji in a configuration file"""
    config_dir = GLib.get_user_config_dir()
    config_filename = f"{config_dir}/custom_tags.json"

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

    if not emoji in current_conf:
        current_conf[emoji] = {}

    if not 'tags' in current_conf[emoji]:
        current_conf[emoji]['tags'] = ''

    current_conf[emoji]['tags'] += f', {tags}' if (len(current_conf[emoji]['tags']) > 0) else tags
    
    try:
        result = GLib.file_set_contents(f"{config_dir}/custom_tags.json", json.dumps(current_conf).encode())
        if not result:
            raise Exception()
    except:
        return False

    current_conf_json = GLib.file_get_contents(config_filename)