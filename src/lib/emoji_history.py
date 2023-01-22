import gi
from time import time
from .user_config import read_json_config, save_json_config
from gi.repository import Gtk, Gio, Gdk

history: dict = None

def increment_emoji_usage_counter(button: Gtk.Button):
    global history
    max_history_size = 30
    
    emoji_hexcode = button.hexcode
    history = read_json_config('usage_history')

    if not emoji_hexcode in history:
        history[emoji_hexcode] = {}
        history[emoji_hexcode]['count'] = 0


    history[emoji_hexcode]['count'] += 1
    history[emoji_hexcode]['lastUsage'] = round(time())
    
    if (len(history) > max_history_size):
        sorted_h = dict( sorted(history.items(), key=lambda kv:kv[1]['lastUsage']) )
        older_key = [*sorted_h][0]
        del history[older_key]

    button.recent = True

    save_json_config(history, 'usage_history')


def get_history(cache=True) -> dict:
    global history

    if (history == None):
        history = read_json_config('usage_history')

    return history