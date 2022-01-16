import manimpango
import sys
import gi
from .picker import Picker
from .shortcuts import ShortcutsWindow

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

class Smile(Gtk.Application):
    def __init__(self, **kwargs) -> None:
        super().__init__(application_id="it.mijorus.smile", flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.datadir = kwargs['datadir']
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        manimpango.register_font(self.datadir + '/assets/NotoColorEmoji.ttf')
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/it/mijorus/smile/assets/style.css')
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        

    def do_activate(self):
         # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = Picker(application=self)
            self.window.connect("destroy", Gtk.main_quit)
            self.window.show_all()

        self.create_action("about", self.on_about_action)
        self.window.show_all()
        self.window.present()

    def create_action(self, name, callback):
        """ Add an Action and connect to a callback """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)

    def on_about_action(self, widget, event):
        pass

def main(version: str, datadir: str) -> None:
    app = Smile(version=version, datadir=datadir)
    app.run(sys.argv)