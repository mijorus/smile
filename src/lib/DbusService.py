import gi
from typing import Optional

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, Adw, GLib  # noqa


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

    def __init__(self):
        self.node = Gio.DBusNodeInfo.new_for_xml(DBUS_NODE_XML)

    def connect(self):
        if not self.dbus_connection:
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
