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
from .lib.emoji_list import emojis

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

class Smile(Gtk.Window):
    def __init__(self, datadir):
        super().__init__(title="Smile")
        self.connect('key_press_event', self.quit_on_escape)
        self.datadir = datadir
        self.set_border_width(10)
        self.set_default_size(300, 250)

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path(self.datadir + '/assets/style.css')

        screen = Gdk.Screen.get_default()

        Gtk.StyleContext.add_provider_for_screen(screen, self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        self.query = None

        self.create_emoji_list()

        scrolled.add(self.flowbox)
        self.box.pack_start(scrolled, True, True, 0)
        
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.connect('search_changed', self.search_emoji)
        self.set_focus(self.search_entry)

        self.box.pack_end(self.search_entry, False, True, 0)


        self.add(self.box)
        self.show_all()

    def quit_on_escape(self, widget, event: Gdk.Event):
        if (event.keyval == Gdk.KEY_Escape):
            Gtk.main_quit()

    def create_emoji_button(self, emoji: str):
        button = Gtk.Button()
        button.set_label(emoji)
        button.connect('clicked', self.copy_and_quit)
        
        return button

    def copy_and_quit(self, button: Gtk.Button):
        clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clip.set_text(button.get_label(), -1)
        self.close()

    def search_emoji(self, search_entry: str):
        query = search_entry.get_text()
        self.query = None if (len(query) == 0) else query
        self.flowbox.invalidate_filter()

    def create_emoji_list(self):
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(30)
        self.flowbox.set_min_children_per_line(4)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flowbox.set_filter_func(self.filter_emoji_list, None)
        
        for e in emojis:
            if e['skintone'] == '':
                button = self.create_emoji_button(e['emoji'])
                button.tag = f"{e['annotation']} {e['tags']}".replace(',', '')
                self.flowbox.add(button)

    def filter_emoji_list(self, widget: Gtk.FlowBoxChild, user_data):
        if (self.query == None or ( (widget.get_child()).tag.lower().__contains__(self.query.lower()) )):
            return True

        return False

def main(verison, datadir: str):
    manimpango.register_font(datadir + '/assets/NotoColorEmoji.ttf')

    window = Smile(datadir)
    window.connect("destroy", Gtk.main_quit)
    window.show_all()

    Gtk.main()
