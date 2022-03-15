import manimpango
import sys
import gi
from .utils import make_option
from .Picker import Picker
from .ShortcutsWindow import ShortcutsWindow
from .AboutDialog import AboutDialog
from .Settings import Settings

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GLib

class Smile(Gtk.Application):
    def __init__(self, **kwargs) -> None:
        self.application_id = "it.mijorus.smile"
        super().__init__(application_id=self.application_id, flags=Gio.ApplicationFlags.FLAGS_NONE)

        entries = [
            make_option('start-hidden'),
            make_option('version')
        ]

        self.add_main_option_entries(entries)

        self.datadir = kwargs['datadir']
        self.version = kwargs['version']
        self.start_hidden = False
        self.window = None

    def do_handle_local_options(self, options):
        if options.contains('version'):
            print(self.version)
            return 0

        self.start_hidden = options.contains('start-hidden')
        return -1

    def do_startup(self):
        Gtk.Application.do_startup(self)

        manimpango.register_font(self.datadir + '/assets/NotoColorEmoji.ttf')
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/it/mijorus/smile/assets/style.css')
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.settings = Gio.Settings.new(self.application_id)

    def do_activate(self):
         # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = Picker(application=self)
            self.window.connect("destroy", Gtk.main_quit)

            self.create_action("preferencies", lambda w,e: Settings(self.application_id))
            self.create_action("open_shortcuts", lambda w,e: ShortcutsWindow().open())
            self.create_action("about", self.on_about_action)
            
            if not self.start_hidden:
                self.window.show_all()
                self.window.present()
        else:
            self.window.show_all()
            self.window.present()

    def create_action(self, name, callback):
        """ Add an Action and connect to a callback """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)

    def on_about_action(self, widget, event):
        about = AboutDialog(self.props.active_window, version=self.version)
        about.present()

def main(version: str, datadir: str) -> None:
    app = Smile(version=version, datadir=datadir)
    app.run(sys.argv)