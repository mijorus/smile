import gi
from ..assets.emoji_list import emojis
from ..lib.widget_utils import create_emoji_button, create_flowbox_child
from ..components.EmojiButton import EmojiButton
from .CustomPopover import CustomPopover

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, GLib, Adw  # noqa


class SkintoneSelector(CustomPopover):
    def __init__(self, emoji_button: EmojiButton, parent: Gtk.Window, click_handler: callable, keypress_handler: callable):
        super().__init__(parent=parent)
        self.click_handler = click_handler
        self.emoji_button = emoji_button
        self.flowbox_widgets: list[EmojiButton] = []
        settings: Gio.Settings = Gio.Settings.new('it.mijorus.smile')
        skintone_modifier = settings.get_string('skintone-modifier')

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
            halign=Gtk.Align.CENTER,
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

        emoji_data = self.emoji_button.emoji_data
        relative_widget_hexcode = emoji_data['hexcode']
        available_skintones = [
            emoji_data,
            *emojis[relative_widget_hexcode].get('skintones', [])
        ]

        for skintone in available_skintones:
            if not skintone_modifier and not skintone['skintone']:
                continue

            elif skintone_modifier and (f'-{skintone_modifier}' in skintone['hexcode']):
                continue

            button = EmojiButton()
            button.position = -1
            button.emoji_data = skintone
            button.hexcode = skintone['hexcode']
            button.base_skintone_widget = self.emoji_button
            button.set_label(skintone['emoji'])

            skintone_emojis.append(button)
            self.flowbox_widgets.append(button)

        popover_container.set_child(skintone_emojis)
        popover_content.append(popover_container)

        popover_content.append(
            Gtk.Label(
                label=_("<small>Press Enter to select or ESC to close</small>"),
                use_markup=True,
                margin_top=10,
                css_classes=['dim-label']
            )
        )

        self.set_size_request(-1, -1)
        self.set_content(popover_content)

    def handle_activate(self, event):
        self.click_handler(event)
        return True

    @staticmethod
    def check_skintone(emoji_button: EmojiButton):
        relative_widget_hexcode = emoji_button.hexcode
        relative_widget_hexcode = relative_widget_hexcode.split('-')[0]

        if relative_widget_hexcode in emojis \
            and emojis[relative_widget_hexcode].get('skintones', []):
            return True

        return False
