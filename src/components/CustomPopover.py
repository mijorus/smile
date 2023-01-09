import gi
from typing import Optional

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, GLib, Adw  # noqa


class CustomPopover(Adw.Window):
    def __init__(self, parent: Gtk.Window):
        super().__init__(resizable=False, transient_for=parent, destroy_with_parent=True, modal=True, deletable=False)

        self.event_controller_keys = Gtk.EventControllerKey()
        self.event_controller_keys.connect('key-pressed', self.handle_key_press)
        self.connect('close-request', lambda _: True)
        self.add_controller(self.event_controller_keys)
        self.handle_close: Optional[callable] = None

    def handle_key_press(self, controller: Gtk.EventController, keyval: int, keycode: int, state: Gdk.ModifierType):
        if keyval == Gdk.KEY_Escape:
            self.request_close()
            return True

    def request_close(self):
        if self.handle_close:
            self.handle_close()

        self.destroy()
