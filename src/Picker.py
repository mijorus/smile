# main.py
#
# Copyright 2021 Lorenzo Paderi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
import time
import re

from .assets.emoji_list import emojis, emoji_categories
from .ShortcutsWindow import ShortcutsWindow
from .CustomTagEntry import CustomTagEntry
from .lib.custom_tags import get_custom_tags
from .lib.localized_tags import get_localized_tags
from .lib.emoji_history import increament_emoji_usage_counter, get_history
from .utils import tag_list_contains, is_wayland

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, Adw  # noqa


class EmojiButton(Gtk.Button):
    emoji_button_css = ['emoji-button']
    selected_emoji_button_css = [*emoji_button_css, 'selected']
    active_emoji_button_css = [*emoji_button_css, 'active']

    def __init__(self, data):
        super().__init__(label=data['emoji'], css_classes=self.emoji_button_css)
        self.emoji_data = data
        self.hexcode = data['hexcode']
        self.history = None

    def toggle_select(self):
        self.set_css_classes(self.selected_emoji_button_css)

    def toggle_active(self):
        self.set_css_classes(self.active_emoji_button_css)

    def toggle_deselect(self):
        self.set_css_classes(self.emoji_button_css)


class FlowBoxChild(Gtk.FlowBoxChild):
    emoji_button_css = ['emoji-button']
    selected_emoji_button_css = [*emoji_button_css, 'selected']
    active_emoji_button_css = [*selected_emoji_button_css, 'active']

    def __init__(self, emoji_button: EmojiButton, **kwargs):
        super().__init__(**kwargs)
        self.emoji_button = emoji_button
        self.emoji_button.set_can_focus(False)
        self.emoji_button.emoji_is_selected = False

        self.event_controller_focus = Gtk.EventControllerFocus()
        self.event_controller_focus.connect('enter', self.on_selection)
        self.event_controller_focus.connect('leave', self.on_selection_leave)
        self.add_controller(self.event_controller_focus)

        self.set_child(self.emoji_button)

    def on_selection(self, event):
        self.set_css_classes(['flowbox-selected'])
        self.emoji_button.toggle_active()

    def on_selection_leave(self, event):
        self.set_css_classes([])

        if not self.emoji_button.emoji_is_selected:
            self.emoji_button.toggle_deselect()


class Picker(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Smile", resizable=True, *args, **kwargs)

        self.event_controller_keys = Gtk.EventControllerKey()
        self.event_controller_keys.connect('key-pressed', self.handle_window_key_press)
        self.add_controller(self.event_controller_keys)

        # self.connect('key_press_event', self.handle_window_key_press)
        # self.connect('key_release_event', self.handle_window_key_release)
        self.set_default_size(-1, 350)
        self.settings: Gio.Settings = Gio.Settings.new('it.mijorus.smile')

        self.settings.connect('changed::skintone-modifier', self.update_emoji_skintones)

        self.emoji_grid_col_n = 5
        self.emoji_grid_first_row = []

        self.selected_category_index = 0
        self.selected_category = 'smileys-emotion'
        self.query: str = None
        self.selection: list[str] = []
        self.selected_buttons: list[Gtk.Button] = []
        self.history_size = 0

        self.clipboard = Gdk.Display.get_default().get_clipboard()

        # Create the emoji list and category picker
        self.categories_count = 0
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_size_request(350, 350)
        self.viewport_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, css_classes=['viewport'])

        self.list_tip_revealer = Gtk.Revealer(reveal_child=False)
        self.list_tip_label = Gtk.Label(label='', opacity=0.7, justify=Gtk.Justification.CENTER)
        self.list_tip_revealer.set_child(self.list_tip_label)

        self.emoji_list_widgets: list[FlowBoxChild] = []
        self.emoji_list = self.create_emoji_list()
        self.category_count = 0  # will be set in create_category_picker()
        self.category_picker = self.create_category_picker()
        scrolled.set_child(self.emoji_list)

        self.viewport_box.prepend(self.list_tip_revealer)
        self.viewport_box.prepend(scrolled)
        self.viewport_box.append(self.category_picker)

        # Create an header bar
        self.header_bar = Gtk.HeaderBar()
        self.menu_button = self.create_menu_button()
        self.header_bar.pack_end(self.menu_button)

        # Create search entry
        self.search_entry = self.create_search_entry()

        # self.header_bar.prepend(self.search_entry)
        self.set_titlebar(self.header_bar)

        self.shortcut_window: ShortcutsWindow = None
        self.shift_key_pressed = False

        # Display custom tags at the top of the list when searching
        # This variable the status of the sorted status
        self.list_was_sorted = False

        self.set_child(self.viewport_box)
        self.connect('show', self.on_show)
        self.set_active_category('smileys-emotion')

    def on_hide(self):
        self.search_entry.set_text('')
        self.query = None
        self.selection = []
        self.update_list_tip(None)
        for button in self.selected_buttons:
            button.get_style_context().remove_class('selected')

        self.selected_buttons = []

    def on_activation(self):
        self.present_with_time(time.time())
        self.grab_focus()

        self.set_focus(self.search_entry)

    def on_show(self, widget: Gtk.Window):
        pass

    # Create stuff
    def create_menu_button(self):
        builder = Gtk.Builder()
        builder.add_from_resource('/it/mijorus/smile/ui/menu.xml')
        menu = builder.get_object('primary_menu')

        return Gtk.MenuButton(popover=menu, icon_name='open-menu-symbolic')

    def create_emoji_button(self, data: dict):
        button = EmojiButton(data)
        button.connect('clicked', self.handle_emoji_button_click)
        # button.connect('button_press_event', lambda w, e: self.show_skin_selector(w) if e.button == 3 else None)

        return button

    def create_search_entry(self) -> Gtk.SearchEntry:
        search_entry = Gtk.SearchEntry()
        search_entry.set_hexpand(True)
        # search_entry.props.enable_emoji_completion = False
        search_entry.connect('search_changed', self.search_emoji)
        return search_entry

    def create_category_picker(self) -> Gtk.ScrolledWindow:
        scrolled = Gtk.ScrolledWindow(name='emoji_categories_box')
        box = Gtk.Box(spacing=4)

        i = 0
        for c, cat in emoji_categories.items().__reversed__():
            if 'icon' in cat:
                button = Gtk.Button(valign=Gtk.Align.CENTER)

                button.category = c
                button.index = i
                button.set_label(cat['icon'])
                button.connect('clicked', self.filter_for_category)

                box.prepend(button)
                i += 1

        scrolled.set_child(box)
        # scrolled.get_child().props.margin = 5
        self.categories_count = i
        return scrolled

    def create_emoji_list(self) -> Gtk.FlowBox:
        flowbox = Gtk.FlowBox(valign=Gtk.Align.START,
                              homogeneous=True,
                              name='emoji_list_box',
                              selection_mode=Gtk.SelectionMode.NONE,
                              max_children_per_line=self.emoji_grid_col_n,
                              min_children_per_line=self.emoji_grid_col_n
                              )

        flowbox.set_filter_func(self.filter_emoji_list, None)
        flowbox.set_sort_func(self.sort_emoji_list, None)

        start = time.time_ns()
        for i, e in emojis.items():
            emoji_button = self.create_emoji_button(e)
            flowbox_child = FlowBoxChild(emoji_button)

            is_recent = (e['hexcode'] in get_history())
            flowbox.append(flowbox_child)
            self.emoji_list_widgets.append(flowbox_child)

            if is_recent:
                self.history_size += 1

        print('Emoji list creation took ' + str((time.time_ns() - start) // 1000000) + 'ms')
        return flowbox

    # Handle events
    def handle_emoji_button_click(self, widget: Gtk.Button):
        if (self.shift_key_pressed):
            self.select_button_emoji(widget)
        else:
            self.copy_and_quit(widget)

    # Handle key-presses
    def handle_window_key_release(self, widget, event: Gdk.Event):
        if (event.keyval == Gdk.KEY_Shift_L or event.keyval == Gdk.KEY_Shift_R):
            self.shift_key_pressed = False

    def handle_window_key_press(self, controller: Gtk.EventController, keyval: int, keycode: int, state: Gdk.ModifierType) -> bool:
        """Handle every possible keypress here, returns True if the event was handled (prevent default)"""
        if (keyval == Gdk.KEY_Escape):
            self.default_hiding_action()
            return True

        self.shift_key_pressed = (keyval == Gdk.KEY_Shift_L or keyval == Gdk.KEY_Shift_R)

        ctrl_key = bool(state & Gdk.ModifierType.CONTROL_MASK)
        shift_key = bool(state & Gdk.ModifierType.SHIFT_MASK)
        alt_key = bool(state & Gdk.ModifierType.ALT_MASK)

        is_modifier = ctrl_key or shift_key or alt_key
        string = keycode

        focused_widget = self.get_focus()
        focused_button = None

        if isinstance(focused_widget, FlowBoxChild):
            focused_button = focused_widget.emoji_button

        if self.search_entry.has_focus():
            if (keyval == Gdk.KEY_Down):
                self.emoji_list.get_child_at_pos(0, 0).get_child().grab_focus()
                return True

            return False

        if alt_key:
            if focused_button and keyval == Gdk.KEY_e:
                self.show_skin_selector(focused_button)
                return True
            elif focused_button and keyval == Gdk.KEY_t:
                CustomTagEntry(focused_button)
                return True

        if shift_key:
            if (keyval == Gdk.KEY_Return):
                if focused_button:
                    self.select_button_emoji(focused_button)
                    return True

            elif (keyval == Gdk.KEY_BackSpace):
                if focused_button:
                    if len(self.selection) > 0:
                        last_button = self.selected_buttons[-1]

                        self.selection.pop()
                        self.selected_buttons.pop()

                        if not self.selection.__contains__(last_button.get_label()):
                            last_button.get_style_context().remove_class('selected')
                        self.update_selection_content(self.selection)

                    return True

        if ctrl_key:
            if keyval == Gdk.KEY_Left:
                next_sel = self.selected_category_index - 1 if (self.selected_category_index > 0) else 0
            elif keyval == Gdk.KEY_Right:
                next_sel_index = (self.categories_count - 1)
                next_sel = self.selected_category_index + 1 if (self.selected_category_index < (next_sel_index)) else (next_sel_index)
            elif keyval == Gdk.KEY_question:
                shortcut_window = ShortcutsWindow()
                shortcut_window.open()

            if ('next_sel' in locals()):
                category_picker_box = self.category_picker.get_children()[0].get_children()[0]

                for child in category_picker_box.get_children():
                    if child.index == next_sel:
                        self.filter_for_category(child)
                        break

                return True

            if (keyval == Gdk.KEY_Return):
                if len(self.selection):
                    self.copy_and_quit()
                    return True

        else:
            # Focus is on an emoji button
            if focused_button:
                if (keyval == Gdk.KEY_Return):
                    self.copy_and_quit(focused_button)
                    return True
                elif (keyval == Gdk.KEY_Up):
                    if isinstance(focused_button.props.parent, Gtk.FlowBoxChild) and (focused_button in self.emoji_grid_first_row):
                        self.search_entry.grab_focus()
                        return False
                elif (not is_modifier) and (keycode == 1) and re.match(r'\S', string):
                    self.search_entry.grab_focus()

            # Focus is on a category button
            elif isinstance(focused_widget, Gtk.Button) and hasattr(focused_widget, 'category'):
                # Triggers when we press arrow up on the category picker
                az_re = re.compile(r"[a-z]", re.IGNORECASE)
                if (keyval in [Gdk.KEY_Up, Gdk.KEY_Down, Gdk.KEY_Left, Gdk.KEY_Right]) and re.match(az_re, string):
                    self.search_entry.grab_focus()
                else:
                    if (keyval == Gdk.KEY_Up):
                        self.set_active_category(focused_widget.category)

                        for f in self.emoji_list_widgets:
                            if self.selected_category == 'recents':
                                if f.emoji_button.hexcode in get_history():
                                    f.emoji_button.grab_focus()
                                    break
                            else:
                                if f.emoji_button.emoji_data['group'] == self.selected_category:
                                    print(f.emoji_button.hexcode)
                                    f.emoji_button.grab_focus()
                                    break

                        return True

        return False

    def default_hiding_action(self):
        if (self.settings.get_boolean('iconify-on-esc')):
            self.iconify()
        else:
            self.hide()

        self.on_hide()

    # # # # # #
    def update_list_tip(self, text: str = None):
        if (text is None):
            self.list_tip_revealer.set_reveal_child(False)
        else:
            self.list_tip_label.set_label(text)
            self.list_tip_revealer.set_reveal_child(True)

    def update_selection_content(self, title: str = None):
        self.update_list_tip('Selected: ' + ''.join(title[-8:]))

    def set_active_category(self, category: str):
        for b in []:
            if b.category != category:
                b.get_style_context().remove_class('selected')
            else:
                b.get_style_context().add_class('selected')

    def select_button_emoji(self, button: EmojiButton):
        if not button.emoji_is_selected:
            self.selection.append(button.get_label())
            increament_emoji_usage_counter(button)

            self.selected_buttons.append(button)
            button.emoji_is_selected = True

            button.toggle_select()
            self.update_selection_content(self.selection)

    def hide_skin_selector(self, widget: Gtk.Popover):
        self.emoji_list.set_opacity(1)
        widget.destroy()

    def show_skin_selector(self, widget: Gtk.Button):
        popover = Gtk.Popover(relative_to=widget)
        popover_content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, name='skin_selector', hexpand=True)

        popover_container = Gtk.ScrolledWindow()
        popover_container.set_max_content_width(500)
        popover_container.set_propagate_natural_width(True)
        popover_container.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)

        relative_widget_hexcode = widget.emoji_data['hexcode']
        if ('skintones' in emojis[relative_widget_hexcode]):
            for skintone in emojis[relative_widget_hexcode]['skintones']:
                button = self.create_emoji_button(skintone)
                popover_content.pack_end(button, False, True, 2)
        else:
            label = Gtk.Label(label='No skintones available')
            popover_content.pack_end(label, False, True, 2)

        popover.add(popover_container)
        popover_container.add_with_viewport(popover_content)
        popover_container.show_all()
        popover.popup()

        self.emoji_list.set_opacity(0.5)
        popover.connect('closed', self.hide_skin_selector)
        return True

    def get_first_row(self):
        self.emoji_grid_first_row = []
        for widget in self.emoji_list.get_children():
            if (len(self.emoji_grid_first_row) < self.emoji_grid_col_n) and widget.props.visible:
                self.emoji_grid_first_row.append(widget.get_children()[0])

    def filter_for_category(self, widget: Gtk.Button):
        self.set_active_category(None)
        widget.grab_focus()

        self.query = None
        self.selected_category = widget.category
        self.selected_category_index = widget.index
        self.category_picker.set_opacity(1)

        self.emoji_list.invalidate_filter()

        if widget.category == 'recents':
            self.update_list_tip('Recently used emojis' if (len(get_history())) else "Whoa, it's still empty! \nYour most used emojis will show up here\n")
        elif len(self.selected_buttons) == 0:
            self.update_list_tip(None)

        self.emoji_list.invalidate_sort()
        self.get_first_row()

    def copy_and_quit(self, button: Gtk.Button = None):
        text = ''
        if button:
            text = button.get_label()
            increament_emoji_usage_counter(button)

        contx = Gdk.ContentProvider.new_for_value(''.join([*self.selection, text]))
        self.clipboard.set_content(contx)

        if self.settings.get_boolean('is-first-run'):
            n = Gio.Notification.new('Copied!')
            n.set_body("I have copied the emoji to the clipboard. You can now paste it in any input field.")
            n.set_icon(Gio.ThemedIcon.new('dialog-information'))

            Gio.Application.get_default().send_notification('copy-message', n)
            self.settings.set_boolean('is-first-run', False)

        self.default_hiding_action()

    def search_emoji(self, search_entry: str):
        query = search_entry.get_text().strip()
        if (len(query) == 0):
            self.query = None
            list_was_sorted = False
        else:
            self.query = query
            list_was_sorted = True

        self.emoji_list.invalidate_filter()

        if (self.list_was_sorted != list_was_sorted):
            if query:
                for child in self.emoji_list.get_children():
                    if get_custom_tags((child.get_child().hexcode), True):
                        child.changed()
            else:
                self.emoji_list.invalidate_sort()

        self.list_was_sorted = list_was_sorted

    def filter_emoji_list(self, widget: Gtk.FlowBoxChild, user_data):
        e = (widget.get_child()).emoji_data
        filter_result = True

        localized_tags = []
        if self.settings.get_boolean('use-localized-tags') and self.settings.get_string('tags-locale') != 'en':
            localized_tags = get_localized_tags(self.settings.get_string('tags-locale'), e['hexcode'], Gio.Application.get_default().datadir)

        merge_en_tags = self.settings.get_boolean('use-localized-tags') and self.settings.get_boolean('merge-english-tags')

        if self.query:
            if self.query == e['emoji']:
                filter_result = True
            elif get_custom_tags(e['hexcode'], cache=True) and tag_list_contains(get_custom_tags(e['hexcode'], cache=True), self.query):
                filter_result = True
            elif (not self.settings.get_boolean('use-localized-tags')):
                filter_result = tag_list_contains(e['tags'], self.query)
            elif self.settings.get_boolean('use-localized-tags'):
                if self.settings.get_boolean('merge-english-tags'):
                    filter_result = tag_list_contains(','.join(localized_tags), self.query) or tag_list_contains(e['tags'], self.query)
                else:
                    filter_result = tag_list_contains(','.join(localized_tags), self.query)

            else:
                filter_result = False

        elif self.selected_category:
            if self.selected_category == 'recents':
                filter_result = get_history().__contains__((widget.get_child()).hexcode)
            else:
                filter_result = self.selected_category == e['group']

        else:
            filter_result = e['group'] == self.selected_category

        if filter_result:
            widget.show()
        else:
            widget.hide()

        return filter_result

    def sort_emoji_list(self, child1: Gtk.FlowBoxChild, child2: Gtk.FlowBoxChild, user_data):
        child1 = child1.get_child()
        child2 = child2.get_child()

        if (self.selected_category == 'recents'):
            h1 = get_history()[child1.hexcode] if child1.hexcode in get_history() else None
            h2 = get_history()[child2.hexcode] if child2.hexcode in get_history() else None
            return ((h2['lastUsage'] if h2 else 0) - (h1['lastUsage'] if h1 else 0))

        elif self.query:
            return -1 if get_custom_tags(child1.hexcode, True) else 1

        else:
            return (child1.emoji_data['order'] - child2.emoji_data['order'])

    def update_emoji_skintones(self, settings: Gio.Settings, key):
        modifier_settings = self.settings.get_string('skintone-modifier')
        for child in self.emoji_list.get_children():
            emoji_button = child.get_children()[0]

            if 'skintones' in emoji_button.emoji_data:
                if len(modifier_settings):
                    for tone in emoji_button.emoji_data['skintones']:
                        if f'-{modifier_settings}' in tone['hexcode']:
                            emoji_button.set_label(tone['emoji'])
                            break
                else:
                    emoji_button.set_label(emoji_button.emoji_data['emoji'])
