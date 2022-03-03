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

import sys
import gi
import time
import os
import csv
import re

from .assets.emoji_list import emojis
from .ShortcutsWindow import ShortcutsWindow
from .CustomTagEntry import CustomTagEntry
from .lib.custom_tags import get_custom_tags
from .lib.emoji_history import increament_emoji_usage_counter, get_history
from .utils import tag_list_contains

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

class Picker(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(title="Smile", resizable=False, border_width=5, *args, **kwargs)
        self.connect('key_press_event', self.handle_window_key_press)
        self.connect('key_release_event', self.handle_window_key_release)
        self.set_default_size(200, 350)
        self.set_position(Gtk.WindowPosition.MOUSE)

        self.settings = Gio.Settings.new('it.mijorus.smile')
        self.settings.connect('changed::open-on-mouse-position', lambda s,key: 
            self.set_position(Gtk.WindowPosition.MOUSE) if s.get_boolean('open-on-mouse-position') else self.set_position(Gtk.WindowPosition.CENTER)
        )

        self.emoji_grid_col_n = 5
        
        self.selected_category_index = 0
        self.selected_category = 'smileys-emotion'
        self.query: str = None
        self.selection: List[str] = []
        self.selected_buttons: List[Gtk.Button] = []
        self.history_size = 0

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        # Create the emoji list and category picker
        self.categories_count = 0
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.viewport_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.list_tip_container = Gtk.Revealer(reveal_child=False)
        self.list_tip_container.add(Gtk.Label(label='', opacity=0.7, justify=Gtk.Justification.CENTER))
        
        self.emoji_list = self.create_emoji_list()
        self.category_count = 0 # will be set in create_category_picker()
        self.category_picker = self.create_category_picker()

        self.emoji_list_container = Gtk.Revealer(reveal_child=True, transition_type=Gtk.RevealerTransitionType.SLIDE_RIGHT, transition_duration=200)
        self.emoji_list_container.add(self.emoji_list)
        scrolled.add(self.emoji_list_container)

        self.viewport_box.pack_start(self.list_tip_container, False, False, 0)
        self.viewport_box.pack_start(scrolled, True, True, 0)
        self.viewport_box.pack_end(self.category_picker, False, True, 3)
        
        # Create an header bar
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.props.show_close_button = True
        self.menu_button = self.create_menu_button()
        self.header_bar.pack_end(self.menu_button)
        
        # Create search entry
        self.search_entry = self.create_search_entry()
        
        self.header_bar.pack_start(self.search_entry)
        self.set_titlebar(self.header_bar)

        self.shortcut_window: ShortcutsWindow = None
        self.shift_key_pressed = False

        # Display custom tags at the top of the list when searching
        # This variable the status of the sorted status
        self.list_was_sorted = False

        self.add(self.viewport_box)
        self.connect('show', self.on_show)
        self.connect('hide', self.on_hide)

    def on_hide(self, widget: Gtk.Widget):
        self.search_entry.set_text('')
        self.query = None
        self.selection = []
        self.update_list_tip(None)
        for button in self.selected_buttons:
            button.get_style_context().remove_class('selected')

        self.selected_buttons = []

    def on_show(self, widget: Gtk.Window):
        self.set_focus(self.search_entry)

    # Create stuff
    def create_menu_button(self):
        builder = Gtk.Builder()
        builder.add_from_resource('/it/mijorus/smile/ui/menu.xml')
        menu = builder.get_object('primary_menu')

        return Gtk.MenuButton(popover=menu, image=Gtk.Image.new_from_icon_name('open-menu-symbolic', Gtk.IconSize.MENU), use_popover = True)

    def create_emoji_button(self, data: dict):
        button = Gtk.Button()
        button.set_label(data['emoji'])
        button.emoji_data = data
        button.hexcode = data['hexcode']
        button.history = get_history()[data['hexcode']] if (data['hexcode']) in get_history() else None
        # button.tag = f"{data['annotation']} {data['tags']}".replace(',', ' ')
        if 'skintones' in data:
            button.get_style_context().add_class('emoji-with-skintones')

        button.connect('clicked', self.handle_emoji_button_click)
        button.connect('button_press_event', lambda w, e: self.show_skin_selector(w) if e.button == 3 else None)

        return button

    def create_search_entry(self) -> Gtk.SearchEntry:
        search_entry = Gtk.SearchEntry()
        search_entry.set_hexpand(True)
        search_entry.connect('search_changed', self.search_emoji)
        return search_entry

    def create_category_picker(self) -> Gtk.ScrolledWindow:
        scrolled = Gtk.ScrolledWindow(name='emoji_categories_box')
        box = Gtk.Box()

        i = 0
        for c, cat in self.get_emoji_category().items():
            if 'icon' in cat:

                button = Gtk.Button(valign=Gtk.Align.CENTER)
                button.category = c
                button.index = i
                button.set_label(cat['icon'])
                button.connect('clicked', self.filter_for_category)

                box.pack_start(button, True, True, 3)
                i += 1

        scrolled.add(box)
        scrolled.get_children()[0].props.margin = 5
        self.categories_count = i
        return scrolled

    def create_emoji_list(self) -> Gtk.FlowBox:
        flowbox = Gtk.FlowBox(valign=Gtk.Align.START, homogeneous=True, name='emoji_list_box', selection_mode=Gtk.SelectionMode.NONE,
            max_children_per_line=self.emoji_grid_col_n, min_children_per_line=self.emoji_grid_col_n
        )

        flowbox.set_filter_func(self.filter_emoji_list, None)
        flowbox.set_sort_func(self.sort_emoji_list, None)

        start = time.time_ns() // 1000000
        for i, e in emojis.items():
            flowbox_child = Gtk.FlowBoxChild()
            flowbox_child.props.can_focus = False

            is_recent = (e['hexcode'] in get_history())
            button = self.create_emoji_button(e)
            flowbox_child.add(button)
            flowbox.add(flowbox_child)

            if is_recent:
                self.history_size += 1

        print('Emoji list creation took ' + str((time.time_ns() // 1000000) - start) + 'ms')
        return flowbox

    # Other methods
    def handle_emoji_button_click(self, widget: Gtk.Button):
        if (self.shift_key_pressed):
            self.select_button_emoji(widget)
        else:
            self.copy_and_quit(widget)

    def update_list_tip(self, text: str = None):
        if (text == None):
            self.list_tip_container.set_reveal_child(False)
        else:
            self.list_tip_container.get_children()[0].set_label(text)
            self.list_tip_container.set_reveal_child(True)

    def update_selection_content(self, title: str = None):
        self.update_list_tip('Selected: ' + ''.join(title[-8:]))

    def set_active_category(self, category: str):
        for b in self.category_picker.get_children()[0].get_children()[0].get_children():
            if b.category != category:
                b.get_style_context().remove_class('selected')
            else:
                b.get_style_context().add_class('selected')

    def select_button_emoji(self, button: Gtk.Button):
        self.selection.append(button.get_label())
        increament_emoji_usage_counter(button)

        self.selected_buttons.append(button)
        button.get_style_context().add_class('selected')
        self.update_selection_content(self.selection)

    def handle_window_key_release(self, widget, event: Gdk.Event):
        if (event.keyval == Gdk.KEY_Shift_L or event.keyval == Gdk.KEY_Shift_R):
            self.shift_key_pressed = False

    def handle_window_key_press(self, widget, event: Gdk.Event):
        """Handle every possible keypress here"""
        if (event.keyval == Gdk.KEY_Escape):
            self.hide()
            return True

        self.shift_key_pressed = (event.keyval == Gdk.KEY_Shift_L or event.keyval == Gdk.KEY_Shift_R)

        ctrl_key = bool(event.state & Gdk.ModifierType.CONTROL_MASK)
        shift_key = bool(event.state & Gdk.ModifierType.SHIFT_MASK)
        alt_key = bool(event.state & Gdk.ModifierType.MOD1_MASK)

        focused_widget = self.get_focus()
        focused_button = focused_widget if isinstance(focused_widget, Gtk.Button) and hasattr(focused_widget, 'emoji_data') else None

        if self.search_entry.has_focus():
            if (event.keyval == Gdk.KEY_Down):
                self.emoji_list.get_child_at_pos(0, 0).get_child().grab_focus()
                return True

            return False

        if alt_key:
            if focused_button and event.keyval == Gdk.KEY_e:
                self.show_skin_selector(focused_button)
                return True
            elif focused_button and event.keyval == Gdk.KEY_t:
                CustomTagEntry(focused_button)
                return True

        if shift_key:
            if (event.keyval == Gdk.KEY_Return):
                if focused_button:
                    self.select_button_emoji(focused_button)
                    return True

            elif (event.keyval == Gdk.KEY_BackSpace):
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
            if event.keyval == Gdk.KEY_Left:
                next_sel = self.selected_category_index - 1 if (self.selected_category_index > 0) else 0
            elif event.keyval == Gdk.KEY_Right:
                next_sel_index = (self.categories_count - 1)
                next_sel = self.selected_category_index + 1 if (self.selected_category_index < (next_sel_index)) else (next_sel_index)
            elif event.keyval == Gdk.KEY_question:
                shortcut_window = ShortcutsWindow()
                shortcut_window.open()
                
            if ('next_sel' in locals()):
                category_picker_box = self.category_picker.get_children()[0].get_children()[0]
                
                for child in category_picker_box.get_children():
                    if child.index == next_sel:
                        self.filter_for_category(child)
                        break

                return True

            if (event.keyval == Gdk.KEY_Return):
                if len(self.selection):
                    self.copy_and_quit()
                    return True

        else:
            if focused_button:
                if (event.keyval == Gdk.KEY_Return):
                    self.copy_and_quit(focused_button)
                    return True
                elif (event.keyval == Gdk.KEY_Up) and isinstance(focused_button.props.parent, Gtk.FlowBoxChild) and (focused_button.props.parent.get_index() < self.emoji_grid_col_n):
                    return False
                elif not event.is_modifier and event.length == 1 and re.match(r'\S', event.string):
                    self.search_entry.grab_focus()

            elif isinstance(focused_widget, Gtk.Button) and hasattr(focused_widget, 'category'):
                # Triggers when we press arrow up on the category picker
                if (event.keyval == Gdk.KEY_Up):
                    self.set_active_category(focused_widget.category)

                    for f in self.emoji_list.get_children():
                        if self.selected_category == 'recents':
                            if f.get_children()[0].hexcode in get_history():
                                f.get_children()[0].grab_focus()
                                break
                        else:
                            if f.get_children()[0].emoji_data['group'] == self.selected_category:
                                f.get_children()[0].grab_focus()
                                break

                    return True

        return False

    def hide_skin_selector(self, widget: Gtk.Popover):
        self.emoji_list.set_opacity(1)
        widget.destroy()

    def show_skin_selector(self, widget: Gtk.Button):
        popover = Gtk.Popover(relative_to=widget)
        popover_content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, name='skin_selector')

        relative_widget_hexcode = widget.emoji_data['hexcode']
        if ('skintones' in emojis[relative_widget_hexcode]):
            for skintone in emojis[relative_widget_hexcode]['skintones']:
                button = self.create_emoji_button(skintone)
                popover_content.pack_end(button, False, True, 2)
        else:
            label = Gtk.Label(label='No skintones available')
            popover_content.pack_end(label, False, True, 2)


        popover.add(popover_content)
        popover_content.show_all()
        popover.popup()

        self.emoji_list.set_opacity(0.5)
        popover.connect('closed', self.hide_skin_selector)
        return True

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

    def copy_and_quit(self, button: Gtk.Button = None):
        clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        text = ''
        if button:
            text = button.get_label()
            increament_emoji_usage_counter(button)

        clip.set_text(''.join([*self.selection, text]), -1)
        self.hide()

    def search_emoji(self, search_entry: str):
        query = search_entry.get_text()
        
        if (len(query) == 0):
            self.query = None
            list_was_sorted = False
        else:
            self.query = query
            list_was_sorted = True

        self.emoji_list.invalidate_filter()
        
        if (self.list_was_sorted != list_was_sorted):
            self.emoji_list.invalidate_sort()

        self.list_was_sorted = list_was_sorted

    def filter_emoji_list(self, widget: Gtk.FlowBoxChild, user_data):
        e = (widget.get_child()).emoji_data
        
        if self.query:
            if get_custom_tags(e['hexcode'], cache=True) and tag_list_contains(get_custom_tags(e['hexcode'], cache=True), self.query):
                return True
            elif tag_list_contains(e['tags'], self.query): 
                return True
            else:
                return False
        
        elif self.selected_category:
            if self.selected_category == 'recents':
                return get_history().__contains__((widget.get_child()).hexcode)

            return self.selected_category == e['group']

        else:
            return e['group'] == self.selected_category

    def sort_emoji_list(self, child1: Gtk.FlowBoxChild, child2: Gtk.FlowBoxChild, user_data):
        child1 = child1.get_child()
        child2 = child2.get_child()

        if (self.selected_category == 'recents'):
            h1 = get_history()[child1.hexcode] if child1.hexcode in get_history() else None
            h2 = get_history()[child2.hexcode] if child2.hexcode in get_history() else None
            return ( (h2['lastUsage'] if h2 else 0) - (h1['lastUsage'] if h1 else 0) )

        elif self.query:
            return -1 if get_custom_tags(child1.hexcode, True) else 1

        else:
            return (child1.emoji_data['order'] - child2.emoji_data['order'])

    def get_emoji_category(self) -> dict:
        return {
            'recents': {
                'icon': '🕖️',
            }, 
            'smileys-emotion': {
                'icon': '😀',
            }, 
            'animals-nature': {
                'icon': '🐶'
            }, 
            'travel-places': {
                'icon': '🚘️'
            }, 
            'activities': {
                'icon': '⚽️'
            }, 
            'objects': {
                'icon': '💡'
            }, 
            'flags': {
                'icon': '🏳️'
            },
        }

