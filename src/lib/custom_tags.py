import json
from gi.repository import GLib
from ..assets.emoji_list import emojis
from .user_config import save_json_config, read_json_config

def set_custom_tags(emoji: str, tags: str):
    """Saves the new tags for a given emoji in a configuration file"""
    current_conf = read_json_config('custom_tags')

    if not emoji in current_conf:
        current_conf[emoji] = {}

    if not 'tags' in current_conf[emoji]:
        current_conf[emoji]['tags'] = ''

    current_conf[emoji]['tags'] += f', {tags}' if (len(current_conf[emoji]['tags']) > 0) else tags

    res = save_json_config(current_conf, 'custom_tags')

def get_custom_tags(hexcode: str) -> str:
    current_conf = read_json_config('custom_tags')

    return current_conf[hexcode]['tags'] if (hexcode in current_conf) else ''