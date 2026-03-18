import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


class EmojiButton(Gtk.Button):
    __gtype_name__ = 'EmojiButton'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position: int = None
        self.emoji_data: dict = None
        self.hexcode: str = None
        self.base_skintone_widget: Gtk.Widget = None
