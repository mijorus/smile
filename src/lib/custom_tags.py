import json
from gi.repository import GLib
from ..assets.emoji_list import emojis
from .user_config import save_json_config, read_json_config

custom_tags_config = None

def set_custom_tags(emoji: str, tags: str):
    global custom_tags_config
    """Saves the new tags for a given emoji in a configuration file"""
    current_conf = read_json_config('custom_tags')

    if not emoji in current_conf:
        current_conf[emoji] = {}

    if not 'tags' in current_conf[emoji]:
        current_conf[emoji]['tags'] = ''

    if (len(tags) == 0):
        del current_conf[emoji]
    else:
        current_conf[emoji]['tags'] = tags if tags.endswith(',') else f'{tags},'

    res = save_json_config(current_conf, 'custom_tags')
    custom_tags_config = current_conf

def get_custom_tags(hexcode: str, cache = False) -> str:
    global custom_tags_config

    if not cache or not custom_tags_config:
        custom_tags_config = read_json_config('custom_tags')

    return custom_tags_config[hexcode]['tags'] if (hexcode in custom_tags_config) else ''

def get_all_custom_tags() -> dict:
    return read_json_config('custom_tags')

def delete_custom_tags(hexcode: str):
    conf = read_json_config('custom_tags')
    result = conf.pop(hexcode, False)

    if (result):
        save_json_config(conf, 'custom_tags')

    custom_tags_config = conf
    return result