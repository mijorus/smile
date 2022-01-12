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
from .lib.emoji_list import emojis

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

class Picker(Gtk.Window):
    def __init__(self):
        super().__init__(title="Smile", resizable=False, border_width=5)
        self.connect('key_press_event', self.handle_window_key_press)
        self.set_default_size(200, 350)
        self.set_position(Gtk.WindowPosition.MOUSE)
        self.emoji_grid_col_n = 6
        
        self.selected_category_index = 0
        self.selected_category = 'smileys-emotion'
        self.query: str = None
        self.selection: List[str] = []
        
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        # Create the emoji list
        self.categories_count = 0
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.emoji_list = self.create_emoji_list()
        self.category_picker = self.create_category_picker()
        scrolled.add(self.emoji_list)
        self.box.pack_start(scrolled, True, True, 0)
        self.box.pack_end(self.category_picker, False, True, 3)
        
        # Create an header bar
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.props.show_close_button = True
        
        # Create search entry
        self.search_entry = self.create_search_entry()
        
        self.header_bar.pack_start(self.search_entry)
        self.set_titlebar(self.header_bar)

        self.add(self.box)
        self.connect('show', self.on_show)

    def on_show(self, widget: Gtk.Window):
        self.search_entry.set_text('')
        self.header_bar.set_title('')
        self.query = None
        self.selection = []
        self.set_focus(self.search_entry)

    def update_header_bar_title(self, title: str):
        self.header_bar.props.subtitle = None
        self.header_bar.set_title(''.join(title[-8:]))

    def select_button_emoji(self, button: Gtk.Button):
        self.selection.append(button.get_label())
        button.get_style_context().add_class('selected')
        self.update_header_bar_title(self.selection)

    def handle_window_key_press(self, widget, event: Gdk.Event):
        ctrl_key = bool(event.state & Gdk.ModifierType.CONTROL_MASK)
        shift_key = bool(event.state & Gdk.ModifierType.SHIFT_MASK)

        focused_widget = self.get_focus()
        focused_button = focused_widget if isinstance(focused_widget, Gtk.Button) and hasattr(focused_widget, 'emoji_data') else None

        if (event.keyval == Gdk.KEY_Escape):
            self.hide()
        
        if self.search_entry.has_focus():
            if (event.keyval == Gdk.KEY_Down):
                self.emoji_list.get_child_at_pos(0, 0).get_child().grab_focus()
                return True
        
        if shift_key:
            if (event.keyval == Gdk.KEY_Return):
                if focused_button:
                    self.select_button_emoji(focused_button)
                    return True

        if ctrl_key:
            if event.keyval == Gdk.KEY_Left:
                next_sel = self.selected_category_index - 1 if (self.selected_category_index > 0) else 0
            elif event.keyval == Gdk.KEY_Right:
                next_sel = self.selected_category_index + 1 if (self.selected_category_index < (self.emoji_grid_col_n - 1)) else (self.emoji_grid_col_n - 1)
                
            if ('next_sel' in locals()): 
                self.filter_for_category(self.category_picker.get_child_at_index(next_sel).get_child())
                return True

            if (event.keyval == Gdk.KEY_Return):
                if len(self.selection):
                    self.copy_and_quit()
                    return True
            
            if (event.keyval == Gdk.KEY_BackSpace):
                if focused_button:
                    if self.selection.__contains__(focused_button.get_label()): 
                        self.selection.remove(focused_button.get_label())

                    if not self.selection.__contains__(focused_button.get_label()): 
                        focused_button.get_style_context().remove_class('selected')

                    return True

        else:
            if focused_button:
                if (event.keyval == Gdk.KEY_Return):
                    self.copy_and_quit(focused_button)
                    return True
                elif (event.keyval == Gdk.KEY_Up) and (focused_button.props.parent.get_index() < self.emoji_grid_col_n):
                    return False
                elif not event.is_modifier and event.length == 1 and re.match(r'\S', event.string):
                    self.search_entry.grab_focus()

        return False

    def show_skin_selector(self, widget: Gtk.Button, event):
        popover = Gtk.Popover(relative_to=widget)
        popover_content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, name='skin_selector')

        button = Gtk.Button(label="😀")
        popover_content.pack_end(button, False, True, 2)
        popover_content.show_all()

        popover.add(popover_content)
        popover.popup()
        
        self.emoji_list.set_opacity(0.5)
        popover.connect('closed', lambda w: self.emoji_list.set_opacity(1))

    def create_emoji_button(self, data: dict):
        button = Gtk.Button()
        button.set_label(data['emoji'])
        button.emoji_data = data
        button.tag = f"{data['annotation']} {data['tags']}".replace(',', ' ')
        button.connect('clicked', self.copy_and_quit)
        button.connect('button_press_event', self.show_skin_selector)

        return button

    def create_search_entry(self) -> Gtk.SearchEntry:
        search_entry = Gtk.SearchEntry()
        search_entry.set_hexpand(True)
        search_entry.connect('search_changed', self.search_emoji)
        return search_entry

    def create_category_picker(self) -> Gtk.FlowBox:
        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_max_children_per_line(self.emoji_grid_col_n)
        flowbox.set_min_children_per_line(self.emoji_grid_col_n)
        flowbox.set_homogeneous(True)
        flowbox.set_name('emoji_categories_box')
        
        for c, cat in self.get_emoji_category().items():
            if 'icon' in cat:
                flowbox_child = Gtk.FlowBoxChild()
                flowbox_child.props.can_focus = False

                button = Gtk.Button()
                button.category = c
                button.set_label(cat['icon'])
                button.connect('clicked', self.filter_for_category)

                flowbox_child.add(button)
                flowbox.add(flowbox_child)

        return flowbox

    def filter_for_category(self, widget: Gtk.Button):
        widget.grab_focus()
        self.query = None
        self.selected_category = widget.category
        self.selected_category_index = widget.props.parent.get_index()
        self.category_picker.set_opacity(1)
        self.emoji_list.invalidate_filter()

    def copy_and_quit(self, button: Gtk.Button = None):
        clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        text = button.get_label() if button else ''
        clip.set_text(''.join([*self.selection, text]), -1)
        self.hide()

    def search_emoji(self, search_entry: str):
        query = search_entry.get_text()
        self.query = None if (len(query) == 0) else query
        self.category_picker.set_opacity(1 if self.query == None else 0.6)
        self.emoji_list.invalidate_filter()

    def create_emoji_list(self):
        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_homogeneous(True)
        flowbox.set_name('emoji_list_box')
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        flowbox.set_filter_func(self.filter_emoji_list, None)
        flowbox.set_max_children_per_line(self.emoji_grid_col_n)
        flowbox.set_min_children_per_line(self.emoji_grid_col_n)

        start = time.time_ns() // 1000000
        for i, e in emojis.items():
            flowbox_child = Gtk.FlowBoxChild()
            flowbox_child.props.can_focus = False

            button = self.create_emoji_button(e)

            flowbox_child.add(button)
            flowbox.add(flowbox_child)

        print('Emoji list parsing took ' + str((time.time_ns() // 1000000) - start) + 'ms')
        return flowbox

    def filter_emoji_list(self, widget: Gtk.FlowBoxChild, user_data):
        e = (widget.get_child()).emoji_data
        
        if self.query:
            return (widget.get_child()).tag.lower().__contains__(self.query.lower())
        
        elif self.selected_category:
            return self.selected_category == e['group']

        else:
            return e['group'] == 'smileys-emotion'

    def get_emoji_category(self) -> dict:
        return {
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

