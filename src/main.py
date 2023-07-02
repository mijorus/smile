import manimpango
import sys
import gi

from .utils import make_option
from .Picker import Picker
from .ShortcutsWindow import ShortcutsWindow
from .Settings import Settings
from .lib.DbusService import DbusService 

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, Adw, GLib  # noqa


class Smile(Adw.Application):
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
        self.last_about_key_pressed = None
        self.about = None
        self.start_hidden = False
        self.window = None

    def do_handle_local_options(self, options):
        if options.contains('version'):
            print(self.version)
            return 0

        self.start_hidden = options.contains('start-hidden')
        return -1

    def do_startup(self):
        Adw.Application.do_startup(self)

        manimpango.register_font(self.datadir + '/assets/NotoColorEmoji.ttf')
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/it/mijorus/smile/assets/style.css')
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.settings = Gio.Settings.new(self.application_id)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = Picker(application=self)

            self.create_action("preferences", lambda w, e: self.on_preferences_action())
            self.create_action("open_shortcuts", lambda w, e: ShortcutsWindow().open())
            self.create_action("open_changelog", lambda w, e: Gtk.UriLauncher.new('https://smile.mijorus.it/changelog').launch())
            self.create_action("translate", lambda w, e: Gtk.UriLauncher.new('https://github.com/mijorus/smile/tree/master/po').launch())

            self.create_action("about", self.on_about_action)

            if not self.start_hidden:
                self.window.show()
                self.window.on_activation()

                last_run_version = int(self.settings.get_string('last-run-version').replace('.', ''))

                # any migration scripts should run here...
                if last_run_version < 240:
                    sd


                self.settings.set_string('last-run-version', self.version)

        else:
            self.window.set_visible(True)
            self.window.on_activation()

    def on_preferences_action(self):
        pref_window = Settings(self.application_id, transient_for=self.window)
        pref_window.present()

    def create_action(self, name, callback):
        """ Add an Action and connect to a callback """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)

    def on_about_action(self, widget, event):
        self.about = Adw.AboutWindow(
            version=self.version,
            comments='An emoji picker',
            application_name='Smile',
            application_icon='it.mijorus.smile',
            developer_name='Lorenzo Paderi',
            website='https://smile.mijorus.it',
            issue_url='https://github.com/mijorus/smile',
            debug_info='Type the answer to life, the universe, and everything',
            copyright='(C) 2022 Lorenzo Paderi\n\nLocalized tags by milesj/emojibase, licensed under the MIT License',
        )

        event_controller_keys = Gtk.EventControllerKey()
        event_controller_keys.connect('key-pressed', self.on_about_key_pressed)
        self.about.add_controller(event_controller_keys)

        self.about.set_translator_credits(_("translator_credits"))
        self.about.add_credit_section('Icon by', ['Roman Morozov'])

        self.about.set_transient_for(self.props.active_window)
        self.about.present()

    def on_about_key_pressed(self, controller, keyval, keycode, state):
        if (self.last_about_key_pressed == '4') and (Gdk.keyval_name(keyval) == '2'):
            self.about.set_application_icon('it.mijorus.smile.crazy')

        self.last_about_key_pressed = Gdk.keyval_name(keyval)

def main(version: str, datadir: str) -> None:
    app = Smile(version=version, datadir=datadir)

    dbus_service = DbusService()
    dbus_service.connect()

    app.run(sys.argv)
