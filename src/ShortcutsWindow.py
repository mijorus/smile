import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw  # noqa


class ShortcutsWindow():
    def __init__(self):
        Adw.init()
        builder = Gtk.Builder()
        builder.add_from_resource('/it/mijorus/smile/ui/shortcuts.ui')
        self.shortcut_window = builder.get_object('shortcuts')

    def open(self, parent=None):
        self.shortcut_window.present(parent)
