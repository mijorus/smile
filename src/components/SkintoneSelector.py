import gi
from ..assets.emoji_list import emojis
from ..lib.custom_tags import set_custom_tags, get_custom_tags
from ..lib.localized_tags import get_localized_tags, get_countries_list
from .CustomPopover import CustomPopover
# from .EmojiButton import EmojiButton
# from .FlowBoxChild import FlowBoxChild

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, GLib, Adw  # noqa


class SkintoneSelector(CustomPopover):
    def __init__(self, flowbox_child: Gtk.FlowBoxChild, parent: Gtk.Window, click_handler: callable, keypress_handler: callable, emoji_active_selection: list[Gtk.Button]):
        super().__init__(parent=parent)
        self.click_handler = click_handler
        self.flowbox_child = flowbox_child

        popover_content = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            margin_top=5,
            margin_bottom=5,
            margin_start=5,
            margin_end=5,
        )

        skintone_emojis = Gtk.FlowBox(
            orientation=Gtk.Orientation.HORIZONTAL,
            max_children_per_line=100,
            min_children_per_line=100,
            hexpand=True,
            margin_top=5,
            margin_bottom=5,
            margin_start=2,
            margin_end=2,
        )

        event_controller_keys = Gtk.EventControllerKey()
        event_controller_keys.connect('key-pressed', keypress_handler)
        skintone_emojis.add_controller(event_controller_keys)

        skintone_emojis.set_size_request(250, -1)

        popover_container = Gtk.ScrolledWindow()
        popover_container.set_max_content_width(350)
        popover_container.set_propagate_natural_width(True)
        popover_container.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)

        relative_widget_hexcode = flowbox_child.get_child().emoji_data['hexcode']
        for skintone in emojis[relative_widget_hexcode]['skintones']:
            button = Gtk.Button(label=skintone['emoji'], width_request=55)
            button.base_skintone_widget = flowbox_child
            button.hexcode = skintone['hexcode']

            button.connect('clicked', self.handle_activate)

            child = Gtk.FlowBoxChild(child=button)

            for e in emoji_active_selection:
                if e.hexcode == button.emoji_data['hexcode']:
                    # TODO:
                    # child.set_as_selected()
                    break

            skintone_emojis.append(child)

        popover_container.set_child(skintone_emojis)
        popover_content.append(popover_container)

        popover_content.append(
            Gtk.Label(
                label="<small>Press Enter to select or ESC to close</small>",
                use_markup=True,
                margin_top=10,
                css_classes=['dim-label']
            )
        )

        self.handle_close = self.on_close

        self.set_content(popover_content)
        self.show()

    def handle_activate(self, event):
        self.click_handler(event)
        return True

    def check_skintone(flowbox_child):
        relative_widget_hexcode = flowbox_child.get_child().emoji_data['hexcode']
        if ('skintones' in emojis[relative_widget_hexcode]):
            for skintone in emojis[relative_widget_hexcode]['skintones']:
                return True

        return False

    def on_close(self):
        pass
