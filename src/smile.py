import manimpango
import gi
from .picker import Picker

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

class Smile(Gtk.Application):
    def __init__(self, version: str, datadir: str) -> None:
        super().__init__(application_id="it.mijorus.smile")
        self.datadir = datadir

    def do_startup(self):
        # manimpango.register_font(self.datadir + '/assets/NotoColorEmoji.ttf')
        return
        # css_provider = Gtk.CssProvider()
        # css_provider.load_from_path(self.datadir + '/assets/style.css')
        # Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def do_activate(self):
        window = Picker()
        window.show_all()

    def do_shutdown(self):
        return