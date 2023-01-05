import gi
from .CustomTagEntry import CustomTagEntry

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, Adw  # noqa


class EmojiButton(Gtk.Button):
    emoji_button_css = ['emoji-button']
    selected_emoji_button_css = [*emoji_button_css, 'selected']
    active_emoji_button_css = [*emoji_button_css, 'active']

    def __init__(self, data):
        super().__init__(label=data['emoji'], css_classes=self.emoji_button_css)
        self.emoji_data = data
        self.hexcode = data['hexcode']
        self.history = None

    def toggle_select(self):
        self.set_css_classes(self.selected_emoji_button_css)

    def toggle_active(self):
        self.set_css_classes(self.active_emoji_button_css)

    def toggle_deselect(self):
        self.set_css_classes(self.emoji_button_css)