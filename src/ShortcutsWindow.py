import sys
import gi
import time
import os
import csv
import re
from .assets.emoji_list import emojis

gi.require_version('Gtk', '4.0')

from gi.repository import Gtk, Gio, Gdk  # noqa

class ShortcutsWindow():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_resource('/it/mijorus/smile/ui/shortcuts.ui')
        self.shortcut_window = builder.get_object('shortcuts')
        self.shortcut_window.set_default_size(600, 400)

    def open(self):
        self.shortcut_window.present()
