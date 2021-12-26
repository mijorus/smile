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
from .lib.emoji_list import emojis

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

class Picker(Gtk.Window):
    def __init__(self):
        super().__init__(title="Smile")
        self.connect('key_press_event', self.quit_on_escape)
        self.set_border_width(5)
        self.set_default_size(200, 250)
        self.set_resizable(True)
        self.set_position(Gtk.WindowPosition.MOUSE)
        
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        # Create the emoji list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.query = None

        self.emoji_list = self.create_emoji_list()
        scrolled.add(self.emoji_list)
        self.box.pack_start(scrolled, True, True, 0)
        
        # Create an header bar
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_title('Emoji picker')
        self.header_bar.props.subtitle = 'Select an emoji or use the search bar'
        self.header_bar.props.show_close_button = True
        

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_hexpand(True)
        self.search_entry.connect('search_changed', self.search_emoji)
        
        self.header_bar.pack_start(self.search_entry)
        self.set_focus(self.search_entry)
        self.set_titlebar(self.header_bar)

        self.add(self.box)

    def quit_on_escape(self, widget, event: Gdk.Event):
        if (event.keyval == Gdk.KEY_Escape):
            Gtk.main_quit()

    def create_emoji_button(self, emoji: str):
        box = Gtk.Box()

        button = Gtk.Button()
        button.set_label(emoji)
        button.connect('clicked', self.copy_and_quit)

        box.add(button)
        
        return box

    def copy_and_quit(self, button: Gtk.Button):
        clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clip.set_text(button.get_label(), -1)
        Gtk.main_quit()

    def search_emoji(self, search_entry: str):
        query = search_entry.get_text()
        self.query = None if (len(query) == 0) else query
        self.flowbox.invalidate_filter()

    def create_emoji_list(self):
        # self.flowbox = Gtk.FlowBox()
        # self.flowbox.set_valign(Gtk.Align.START)
        # self.flowbox.set_max_children_per_line(5)
        # self.flowbox.set_min_children_per_line(5)
        # self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        # self.flowbox.set_filter_func(self.filter_emoji_list, None)
        emoji_grid = Gtk.Grid()
            
        row = 0
        col = 0
        for e in emojis:
            if e['skintone'] == '':
                button = self.create_emoji_button(e['emoji'])
                button.tag = f"{e['annotation']} {e['tags']}".replace(',', '')
                
                # self.flowbox.add(fb_child)
                emoji_grid.attach(button, col, row, 1, 1)

                col = col + 1 if col < 5 else 0
                row += 1 if col == 5 else 0
        
        return emoji_grid

    def filter_emoji_list(self, widget: Gtk.FlowBoxChild, user_data):
        if (self.query == None or ( (widget.get_child()).tag.lower().__contains__(self.query.lower()) )):
            return True

        return False


