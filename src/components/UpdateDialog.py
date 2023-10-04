import gi
from typing import Optional

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, GLib, Adw  # noqa


class UpdateDialog():
    new_features_messages = [
        # (from version, to version, message)
        (0, 240, '- Automatically paste emojis on X11 systems and with the GNOME extension on Wayland!'),
        (240, 280, '- Added an option to select multiple emojis on mouse click')
    ]

    @staticmethod
    def show(parent, last_run_version, current_version):
        modal_messages = []
        dialog: Optional[Adw.MessageDialog] = None

        for m in UpdateDialog.new_features_messages:
            if last_run_version >= m[0] and last_run_version < m[1]:
                modal_messages.append(m[2])

        if modal_messages:
            dialog = Adw.MessageDialog.new(
                parent, 
                _('New features!'),
                '\n'.join(modal_messages),
            )

            dialog.add_response('dismiss', _('Dismiss'))
            dialog.set_close_response('dismiss')

            dialog.present()


        