import gi
import time
import re
from .EmojiButton import EmojiButton

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, Adw  # noqa


class FlowBoxChild(Gtk.FlowBoxChild):
    def __init__(self, emoji_button: EmojiButton, **kwargs):
        super().__init__(**kwargs)
        # self.emoji_button = emoji_button
        # self.emoji_button.set_can_focus(False)

        # self._is_selected = False
        # self.event_controller_focus = Gtk.EventControllerFocus()

        # self.default_css = ['flowbox-child-custom']
        # if ('skintones' in emoji_button.emoji_data) and emoji_button.emoji_data['skintones']:
        #     self.default_css.append('emoji-with-skintones')

        # self.set_css_classes(self.default_css)
        
        # self.event_controller_focus.connect('enter', lambda x: self.set_css_classes(self.default_css))
        # self.event_controller_focus.connect('leave', self.on_selection_leave)
        # self.add_controller(self.event_controller_focus)

        self.set_child(emoji_button)

    def on_selection_leave(self, event):
        if self._is_selected:
            self.set_as_selected()
        else:
            self.deselect()

    def set_as_selected(self):
        self._is_selected = True
        self.set_css_classes([*self.default_css, 'selected'])

    def set_as_active(self):
        self.set_css_classes([*self.default_css, 'active'])

    def deselect(self):
        self._is_selected = False
        self.set_css_classes([*self.default_css])
