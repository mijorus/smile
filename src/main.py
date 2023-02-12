import manimpango
import sys
import gi
import time
import dbus

from dbus.mainloop.glib import DBusGMainLoop
from .utils import make_option
from .Picker import Picker
from .ShortcutsWindow import ShortcutsWindow
# from .AboutDialog import AboutDialog
from .Settings import Settings

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, Adw  # noqa

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

            self.create_action("preferences", lambda w, e: Settings(self.application_id))
            self.create_action("open_shortcuts", lambda w, e: ShortcutsWindow().open())
            self.create_action("open_changelog", lambda w, e: Gtk.show_uri(None, 'https://smile.mijorus.it/changelog', time.time()))
            self.create_action("about", self.on_about_action)

            if not self.start_hidden:
                self.window.show()
                self.window.on_activation()

                # create message dialog
                try:
                    last_run_version = self.settings.get_string('last-run-version') or '0.0.0'
                    last_run_version_split = last_run_version.split('.')
                    
                    if last_run_version_split[0] != self.version.split('.')[0] or last_run_version_split[1] != self.version.split('.')[1]:
                        dialog = Gtk.MessageDialog(
                            transient_for=self.window,
                            message_type=Gtk.MessageType.INFO,
                            buttons=Gtk.ButtonsType.OK,
                        )

                        if self.version == '2.0.0':
                            dialog.set_markup(f"""Smile was updated to version {self.version}!\n\n<b>LOTS OF THINGS HAVE CHANGED</b>, including some keyboard shortcuts!\n\nPlease see the changelog on <b>Menu > What's new</b>\nor visit smile.mijorus.it/changelog""")
                        else:
                            dialog.set_markup(f"Smile was updated to version {self.version}!\n\nSee the changelog on <b>Menu > What's new</b>\nor visit smile.mijorus.it/changelog")

                        dialog.connect('response', lambda x, y: dialog.destroy())
                        dialog.show()

                    self.settings.set_string('last-run-version', self.version)
                except Exception as e:
                    print(e)

        else:
            self.window.set_visible(True)
            self.window.on_activation()

    def create_action(self, name, callback):
        """ Add an Action and connect to a callback """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)

    def on_about_action(self, widget, event):
        about = Adw.AboutWindow(
            version=self.version,
            comments='An emoji picker',
            application_name='Smile',
            application_icon='it.mijorus.smile',
            developer_name='Lorenzo Paderi',
            website='https://smile.mijorus.it',
            issue_url='https://github.com/mijorus/smile',
            copyright='(C) 2022 Lorenzo Paderi\n\nLocalized tags by milesj/emojibase, licensed under the MIT License',
        )

        about.add_credit_section('Icon by', ['Roman Morozov'])

        about.set_transient_for(self.props.active_window)
        about.present()

def main(version: str, datadir: str) -> None:
    app = Smile(version=version, datadir=datadir)
    app.run(sys.argv)
