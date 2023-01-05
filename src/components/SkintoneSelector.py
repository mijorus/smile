import gi
from ..assets.emoji_list import emojis
from ..lib.custom_tags import set_custom_tags, get_custom_tags
from ..lib.localized_tags import get_localized_tags, get_countries_list
from .CustomPopover import CustomPopover
from .EmojiButton import EmojiButton

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, GLib, Adw  # noqa


class SkintoneSelector(CustomPopover):
    def __init__(self, flowbox_child: Gtk.FlowBoxChild, parent: Gtk.Window):
        super().__init__(parent=parent)

        popover_content = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, 
            hexpand=True,
            margin_top=5,
            margin_bottom=5,
            margin_start=5,
            margin_end=5,
        )
        
        skintone_emojis = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, hexpand=True, spacing=5)

        popover_container = Gtk.ScrolledWindow()
        popover_container.set_max_content_width(500)
        popover_container.set_propagate_natural_width(True)
        popover_container.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)

        relative_widget_hexcode = flowbox_child.emoji_button.emoji_data['hexcode']
        for skintone in emojis[relative_widget_hexcode]['skintones']:
            button = EmojiButton(skintone, width_request=55)
            skintone_emojis.append(button)
            
        popover_content.append(skintone_emojis)

        popover_content.append(
            Gtk.Label(label="<small>Press Enter or ESC to close without saving</small>", use_markup=True, margin_top=10, css_classes=['dim-label'])
        )

        self.set_content(popover_content)
        self.show()

    def handle_activate(self, user_data):
        set_custom_tags(self.relative_widget_hexcode, self.entry.get_text())
        self.destroy()
        return True

    def check_skintone(flowbox_child):
        relative_widget_hexcode = flowbox_child.emoji_button.emoji_data['hexcode']
        if ('skintones' in emojis[relative_widget_hexcode]):
            for skintone in emojis[relative_widget_hexcode]['skintones']:
                return True

        return False
