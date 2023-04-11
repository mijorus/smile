import gi
from .CustomTagEntry import CustomTagEntry

gi.require_version('Gtk', '4.0')

from gi.repository import Gtk, Gio  # noqa


class EmojiButton(Gtk.Button):
    def __init__(self, data: dict, **kwargs):
        super().__init__(label=data['emoji'], **kwargs)

        self.app_settings = Gio.Settings.new('it.mijorus.smile')

        self.emoji_data = data
        self.hexcode = data['hexcode']
        self.history = None
        
        self.base_skintone_widget = None

        self.update_css_classes()

        self.app_settings.connect('changed::emoji-size-class', lambda w, val: self.update_css_classes())

    def update_css_classes(self):
        self.emoji_button_css = [self.app_settings.get_string('emoji-size-class')]

        if ('skintones' in self.emoji_data) and self.emoji_data['skintones']:
            self.emoji_button_css.append('emoji-with-skintones')
            
        self.set_css_classes(self.emoji_button_css)
