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
import manimpango
import os
import csv

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

class Smile(Gtk.Window):
    def __init__(self, datadir):
        super().__init__(title="Smile")
        self.set_border_width(10)
        self.datadir = datadir
        self.set_default_size(300, 250)


        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.query = None

        csv_emojis = open(self.datadir + '/assets/NotoColorEmoji.ttf', 'r')
        self.emoji_list = csv.reader(csv_emojis)
        # csv_emojis.close()

        self.create_emoji_list()

        scrolled.add(self.flowbox)
        self.box.pack_start(scrolled, True, True, 0)
        
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.connect('search_changed', self.search_emoji)

        self.box.pack_end(self.search_entry, False, True, 0)

        self.add(self.box)
        self.show_all()

    def create_emoji_button(self, emoji):
        button = Gtk.Button()
        button.set_label(emoji)

        return button

    def search_emoji(self, search_entry):
        query = search_entry.get_text()
        self.query = None if (len(query) == 0) else query
        self.flowbox.invalidate_filter()

    def create_emoji_list(self):
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(30)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flowbox.set_filter_func(self.filter_emoji_list, None)
        
        emojis = {
            '😀': 'smile',
            '😃': 'smile',
            '😄': 'laught',
            '😁': 'smile',
            '😆': 'cry',
            '😅': 'drop',
        }

        for e, tag in self.emoji_list:
            button = self.create_emoji_button(e)
            button.tag = tag
            self.flowbox.add(button)

    def filter_emoji_list(self, child, user_data):
        print((self.query))
        if (self.query == None):
            return True
        
        return False

def main(verison, datadir):
    manimpango.register_font(datadir + '/assets/NotoColorEmoji.ttf')

    window = Smile(datadir)
    window.connect("destroy", Gtk.main_quit)
    window.show_all()

    Gtk.main()
