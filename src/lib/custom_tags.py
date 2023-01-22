from gi.repository import GLib
from .user_config import save_json_config, read_json_config

custom_tags_config = None

def set_custom_tags(hexcode: str, tags: str):
    """Saves the new tags for a given emoji in a configuration file"""
    global custom_tags_config

    current_conf = read_json_config('custom_tags')

    if not hexcode in current_conf:
        current_conf[hexcode] = {}

    if not 'tags' in current_conf[hexcode]:
        current_conf[hexcode]['tags'] = ''

    if (len(tags) == 0):
        del current_conf[hexcode]
    else:
        current_conf[hexcode]['tags'] = tags if tags.endswith(',') else f'{tags},'

    res = save_json_config(current_conf, 'custom_tags')
    custom_tags_config = current_conf

def get_custom_tags(hexcode: str, cache=False) -> str:
    global custom_tags_config

    if (not cache) or (not custom_tags_config):
        custom_tags_config = read_json_config('custom_tags')
        
    if (hexcode in custom_tags_config) and custom_tags_config[hexcode]['tags']:
        return custom_tags_config[hexcode]['tags']
    
    return ''

def get_all_custom_tags() -> dict:
    return read_json_config('custom_tags')

def delete_custom_tags(hexcode: str) -> dict:
    global custom_tags_config

    conf = read_json_config('custom_tags')

    if 'tags' in conf[hexcode]:
        conf[hexcode]['tags'] = None

    save_json_config(conf, 'custom_tags')
    custom_tags_config = conf

    return True