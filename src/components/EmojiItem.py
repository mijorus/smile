import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, GObject

# 1. Define a GObject subclass to hold your data
class EmojiItem(GObject.Object):
    __gtype_name__ = 'EmojiItem'

    def __init__(self, emoji: dict, skintone: str):
        super().__init__()
        self.emoji = emoji
        self.skintone = skintone
