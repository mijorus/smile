import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw  # noqa


class MouseControlsDialog():
    def __init__(self):
        Adw.init()
        builder = Gtk.Builder()
        builder.add_from_resource('/it/mijorus/smile/ui/mouse_controls.ui')
        self.dialog = builder.get_object('mouse_controls_dialog')

        settings = Gio.Settings.new('it.mijorus.smile')

        add_em_to_selection_label = _('Add an emoji to selection')
        copy_quit_label = _('Copy the selected emoji and hide the window')

        mouse_multi_select = settings.get_boolean('mouse-multi-select')
        builder.get_object('shift-left-click-row').set_title(copy_quit_label if mouse_multi_select else add_em_to_selection_label)
        builder.get_object('left-click-row').set_title(add_em_to_selection_label if mouse_multi_select else copy_quit_label)

    def open(self, parent=None):
        self.dialog.present(parent)
