import manimpango
import sys
import gi
from .assets.emoji_list import emojis
from .lib.custom_tags import set_custom_tags, get_custom_tags


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GLib

class CustomTagEntry(Gtk.Popover):
    def __init__(self, widget: Gtk.Button):
        super().__init__(relative_to=widget)
        popover_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, name='custom_tag_entry')
        self.relative_widget_hexcode = widget.emoji_data['hexcode']

        max_tags_lengh = 30
        default_tags = emojis[self.relative_widget_hexcode]['tags']

        if len(default_tags) > max_tags_lengh:
            default_tags = default_tags[0:max_tags_lengh] + '...'

        entry = Gtk.Entry(text=get_custom_tags(widget.hexcode))
        entry.set_placeholder_text("List of custom tags, separated  by comma") 
        entry.connect('key_press_event', self.handle_key_press)
        popover_content.pack_start(entry, True, True, 0)

        label = Gtk.Label(f"<small><b>Default tags</b>: {default_tags}</small>", use_markup=True)
        popover_content.pack_end(label, True, True, 0)

        self.add(popover_content)
        popover_content.show_all()
        self.popup()

        self.connect('closed', self.close)

    def handle_key_press(self, widget: Gtk.Entry, event):
        if event.keyval == Gdk.KEY_Return:
            set_custom_tags(self.relative_widget_hexcode, widget.get_text())
            self.destroy()
            return True

    def close(self, widget):
        self.destroy()