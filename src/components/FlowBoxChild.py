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
        self.emoji_button = emoji_button
        self.emoji_button.set_can_focus(False)

        self._is_selected = False
        self.event_controller_focus = Gtk.EventControllerFocus()
        self.set_css_classes(['flowbox-child-custom'])
        self.event_controller_focus.connect('leave', self.on_selection_leave)
        self.lock_status = False
        self.add_controller(self.event_controller_focus)

        self.set_child(self.emoji_button)

    def on_selection(self, event):
        self.set_css_classes(['flowbox-selected'])
        self.emoji_button.set_as_active()

    def on_selection_leave(self, event):
        if self.lock_status:
            return

        if self._is_selected:
            self.set_as_selected()
        else:
            self.deselect()

    def set_as_selected(self):
        self.set_css_classes(['flowbox-child-custom', 'selected'])

    def set_as_active(self):
        self.set_css_classes(['flowbox-child-custom', 'active'])

    def deselect(self):
        self.set_css_classes(['flowbox-child-custom'])
