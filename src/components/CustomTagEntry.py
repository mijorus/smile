import manimpango
import sys
import gi
from ..assets.emoji_list import emojis
from ..lib.custom_tags import set_custom_tags, get_custom_tags
from ..lib.localized_tags import get_localized_tags, get_countries_list
# from .FlowBoxChild import FlowBoxChild


from gi.repository import Gtk, Gio, Gdk, GLib, Adw


class CustomTagEntry(Adw.Window):
    def __init__(self, flowbox_child: Gtk.FlowBoxChild, window):
        super().__init__()

        self.emoji_buttom = flowbox_child.emoji_button

        # self.set_parent(window)
        # alloc = flowbox_child.get_allocation()
        # rect = Gdk.Rectangle(x, y, 0, 0)
        # self.set_pointing_to(rect)
        # print(alloc.x)
        # print(alloc.y)
        # print(window.get_height() - alloc.y)
        # widget.set_child(self)

        popover_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, name='custom_tag_entry')
        self.relative_widget_hexcode = self.emoji_buttom.emoji_data['hexcode']

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

        popover_content.append(
            Gtk.Label(
                label=f'<b>{self.emoji_buttom.emoji_data["emoji"]} Custom tags</b>', 
                use_markup=True, 
                margin_bottom=10
            )
        )

        self.entry = Gtk.Entry(text=get_custom_tags(self.emoji_buttom.hexcode))
        self.entry.set_placeholder_text("List of custom tags, separated  by comma")
        popover_content.append(self.entry)

        self.event_controller_keys = Gtk.EventControllerKey()
        self.event_controller_keys.connect('key-pressed', self.handle_key_press)

        self.entry.add_controller(self.event_controller_keys)
        self.entry.connect('activate', self.handle_activate)

        label_text = f"<small><b>Default tags</b>: {default_tags}</small>"
        if len(localized_tags) > 0:
            label_text += f"\n<small><b>{get_countries_list()[settings.get_string('tags-locale')]['language']} tags</b>: {localized_tags}</small>"

        label = Gtk.Label(label=label_text, use_markup=True, margin_top=10)
        popover_content.append(label)

        self.set_content(popover_content)
        self.show()

        self.connect('close-request', self.close)

    def handle_key_press(self, controller: Gtk.EventController, keyval: int, keycode: int, state: Gdk.ModifierType):
        if keyval == Gdk.KEY_Escape:
            self.destroy()
            return True

    def handle_activate(self, user_data):
        set_custom_tags(self.relative_widget_hexcode, self.entry.get_text())
        self.destroy()
        return True

    def close(self, widget):
        pass
