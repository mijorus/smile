import gi
from .CustomTagEntry import CustomTagEntry

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, Adw  # noqa


class EmojiButton(Gtk.Button):
    def __init__(self, data, **kwargs):
        super().__init__(label=data['emoji'], **kwargs)
        self.emoji_data = data
        self.hexcode = data['hexcode']
        self.history = None
        
        self.emoji_button_css = ['emoji-button']

        if ('skintones' in data) and data['skintones']:
            self.emoji_button_css.append('emoji-with-skintones')
            
        # self.deselect()

    # def set_as_selected(self):
    #     self.get_style_context().remove_class('active')
    #     self.get_style_context().add_class('selected')

    # def set_as_active(self):
    #     self.get_style_context().remove_class('selected')
    #     self.get_style_context().add_class('active')

    # def deselect(self):
    #     self.set_css_classes(self.emoji_button_css)