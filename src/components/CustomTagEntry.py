import gi
from ..assets.emoji_list import emojis
from ..lib.custom_tags import set_custom_tags, get_custom_tags
from ..lib.localized_tags import get_localized_tags, get_countries_list
from .CustomPopover import CustomPopover

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, GLib, Adw  # noqa


class CustomTagEntry(CustomPopover):
    def __init__(self, flowbox_child: Gtk.FlowBoxChild, parent: Gtk.Window):
        super().__init__(parent=parent)

        self.emoji_buttom = flowbox_child.emoji_button
        self.flowbox_child = flowbox_child

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
                label=f'<b>{self.emoji_buttom.emoji_data["emoji"]} Edit custom tags</b>',
                use_markup=True,
                margin_bottom=10,
                css_classes=['heading']
            )
        )

        self.entry = Gtk.Entry(text=get_custom_tags(self.emoji_buttom.hexcode))
        self.entry.set_placeholder_text("List of custom tags, separated  by comma")
        popover_content.append(self.entry)

        self.entry.connect('activate', self.handle_activate)
        self.handle_close = self.on_close

        label_text = f"<small><b>Default tags</b>: {default_tags}</small>"
        if len(localized_tags) > 0:
            label_text += f"\n<small><b>{get_countries_list()[settings.get_string('tags-locale')]['language']} tags</b>: {localized_tags}</small>"

        
        label = Gtk.Label(label=label_text, use_markup=True, margin_top=10)
        popover_content.append(label)
        popover_content.append(
            Gtk.Label(label="<small>Press Enter or ESC to close without saving</small>", use_markup=True, margin_top=10, css_classes=['dim-label'])
        )

        self.flowbox_child.lock_status = True
        self.flowbox_child.set_as_selected()

        self.set_content(popover_content)
        self.show()

    def handle_activate(self, user_data):
        set_custom_tags(self.relative_widget_hexcode, self.entry.get_text())
        self.request_close()
        return True

    def on_close(self):
        self.flowbox_child.lock_status = False
        self.flowbox_child.deselect()
