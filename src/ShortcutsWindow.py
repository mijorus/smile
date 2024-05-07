import sys
import gi
import time
import os
import csv
import re

gi.require_version('Gtk', '4.0')

from gi.repository import Gtk, Gio, Gdk  # noqa

class ShortcutsWindow():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_resource('/it/mijorus/smile/ui/shortcuts.ui')
        self.shortcut_window = builder.get_object('shortcuts')
        self.shortcut_window.set_default_size(600, 400)

        settings = Gio.Settings.new('it.mijorus.smile')

        add_em_to_selection_label = _('Add an emoji to selection')
        copy_quit_label = _('Copy the selected emoji and hide the window')

        mouse_multi_select = settings.get_boolean('mouse-multi-select')
        builder.get_object('shift-left-click-label').set_label(copy_quit_label if mouse_multi_select else add_em_to_selection_label)
        builder.get_object('left-click-label').set_label(add_em_to_selection_label if mouse_multi_select else copy_quit_label)

    def open(self):
        self.shortcut_window.present()
