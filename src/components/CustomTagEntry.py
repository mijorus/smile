import manimpango
import sys
import gi
from ..assets.emoji_list import emojis
from ..lib.custom_tags import set_custom_tags, get_custom_tags
from ..lib.localized_tags import get_localized_tags, get_countries_list
# from .FlowBoxChild import FlowBoxChild


from gi.repository import Gtk, Gio, Gdk, GLib


class CustomTagEntry(Gtk.Popover):
    def __init__(self, flowbox_child: Gtk.FlowBoxChild, window: Gtk.Window):
        super().__init__()
        
        widget = flowbox_child.emoji_button
        
        self.set_parent(window)
        alloc = flowbox_child.get_allocation()
        rect = Gdk.Rectangle(alloc.x, (window.get_height() - alloc.y), 0, 0)
        self.set_pointing_to(rect)
        # print(alloc.x)
        # print(alloc.y)
        # print(window.get_height() - alloc.y)
        # widget.set_child(self)

        popover_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, name='custom_tag_entry')
        self.relative_widget_hexcode = widget.emoji_data['hexcode']

        max_tags_lengh = 30
        default_tags = emojis[self.relative_widget_hexcode]['tags']
        localized_tags = []

        settings: Gio.Settings = Gio.Settings.new('it.mijorus.smile')
        if settings.get_boolean('use-localized-tags'):
            tl = get_localized_tags(settings.get_string('tags-locale'), self.relative_widget_hexcode, Gio.Application.get_default().datadir)
            localized_tags = ', '.join(tl)

        if len(default_tags) > max_tags_lengh:
            default_tags = default_tags[0:max_tags_lengh] + '...'

        if len(localized_tags) > max_tags_lengh:
            localized_tags = localized_tags[0:max_tags_lengh] + '...'

        entry = Gtk.Entry(text=get_custom_tags(widget.hexcode))
        entry.set_placeholder_text("List of custom tags, separated  by comma")
        # entry.connect('key_press_event', self.handle_key_press)
        popover_content.append(entry)

        label_text = f"<small><b>Default tags</b>: {default_tags}</small>"
        if len(localized_tags) > 0:
            label_text += f"\n<small><b>{get_countries_list()[settings.get_string('tags-locale')]['language']} tags</b>: {localized_tags}</small>"

        label = Gtk.Label(label=label_text, use_markup=True)
        popover_content.append(label)

        self.set_child(popover_content)
        # popover_content.show()
        # entry.do_focus()
        self.popup()

        self.connect('closed', self.close)

    def handle_key_press(self, widget: Gtk.Entry, event):
        if event.keyval == Gdk.KEY_Return:
            set_custom_tags(self.relative_widget_hexcode, widget.get_text())
            self.destroy()
            return True

    def close(self, widget):
        self.popdown()
        self.unrealize()
        self.unparent()
