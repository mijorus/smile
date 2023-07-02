import gi
from typing import Optional
from ..utils import portal

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, Adw, GLib  # noqa

GNOME_EXTENSION_LINK = 'https://extensions.gnome.org/extension/6093/smile-complementary-extension'
GNOME_EXTENSION_UUID = 'smile-gnome-extension@mijorus.it'

DBUS_SERVICE_INTERFACE = 'it.mijorus.smile'
DBUS_SERVICE_PATH = '/it/mijorus/smile/actions'
DBUS_NODE_XML = """
    <node>"
      <interface name='it.mijorus.smile'>"
        <signal name='CopiedEmoji'>"
          <arg type='s' name='msg'>"
          </arg>"
        </signal>"
      </interface>"
    </node>
"""

class DbusService():
    dbus_connection = None
    extension_status = 'not_installed' # installed, not_installed, unavailable 

    def __init__(self):
        self.node = Gio.DBusNodeInfo.new_for_xml(DBUS_NODE_XML)

        try:
            inter = portal('org.gnome.Shell.Extensions', 'org.gnome.Shell.Extensions', '/org/gnome/Shell/Extensions')
            installed_extensions = [str(k) for k in inter.ListExtensions().keys()]
            DbusService.extension_status = 'installed' if GNOME_EXTENSION_UUID in installed_extensions else 'not_installed'
        except Exception as e:
            DbusService.extension_status = 'unavailable'

    def connect(self):
        if (DbusService.extension_status != 'unavailable') and (not self.dbus_connection):
            Gio.bus_own_name(
                Gio.BusType.SESSION,
                DBUS_SERVICE_INTERFACE,
                Gio.BusNameOwnerFlags.NONE,
                self.on_bus_acquired,
                None,
                None,
            )

    def handle_method_call(self, connection, sender, object_path, interface_name, method_name, params, invocation):
        pass

    def on_bus_acquired(self, connection, name):
        DbusService.dbus_connection = connection

        self.reg_id = connection.register_object(
            DBUS_SERVICE_PATH, self.node.interfaces[0], self.handle_method_call, None, None
        )
