import gi
from .CustomTagEntry import CustomTagEntry

gi.require_version('Gtk', '4.0')

from gi.repository import Gtk  # noqa


class EmojiButton(Gtk.Button):
    def __init__(self, data, **kwargs):
        super().__init__(label=data['emoji'], **kwargs)
        self.emoji_data = data
        self.hexcode = data['hexcode']
        self.history = None
        
        self.base_skintone_widget = None
        
        self.emoji_button_css = ['emoji-button']

        if ('skintones' in data) and data['skintones']:
            self.emoji_button_css.append('emoji-with-skintones')
            
        self.set_css_classes(self.emoji_button_css)