import gi
import time
import re
from .EmojiButton import EmojiButton

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, Adw  # noqa

class FlowBoxChild(Gtk.FlowBoxChild):
    emoji_button_css = ['emoji-button']
    selected_emoji_button_css = [*emoji_button_css, 'selected']
    active_emoji_button_css = [*selected_emoji_button_css, 'active']

    def __init__(self, emoji_button: EmojiButton, **kwargs):
        super().__init__(**kwargs)
        self.emoji_button = emoji_button
        self.emoji_button.set_can_focus(False)
        self.emoji_button.emoji_is_selected = False

        self.event_controller_focus = Gtk.EventControllerFocus()
        self.event_controller_focus.connect('enter', self.on_selection)
        self.event_controller_focus.connect('leave', self.on_selection_leave)
        self.add_controller(self.event_controller_focus)

        self.set_child(self.emoji_button)

    def on_selection(self, event):
        self.set_css_classes(['flowbox-selected'])
        self.emoji_button.toggle_active()

    def on_selection_leave(self, event):
        self.set_css_classes([])

        if not self.emoji_button.emoji_is_selected:
            self.emoji_button.toggle_deselect()