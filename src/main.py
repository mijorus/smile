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

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk

class Smile(Gtk.Window):
    def __init__(self):
        super().__init__(title="Smile")
        self.set_border_width(10)
        self.set_default_size(300, 250)


        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_max_children_per_line(30)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)

        self.create_flowbox(flowbox)

        scrolled.add(flowbox)

        self.add(scrolled)
        self.show_all()

    def create_emoji_button(self, emoji):
        button = Gtk.Button()
        button.set_label(emoji)

        return button


    def create_flowbox(self, flowbox):
        colors = [
            '😀', 
            '😃',
            '😄',
            '😁',
            '😆',
            '😅',
            '😂',
            '🤣',
            '🥲',
            '😊',
            '😇',
            '🙂',
            '🙃',
            '😉',
            '😌',
            '😍',
            '🥰',
            '😘',
            '😗',
            '😙',
            '😚',
        ]

        for color in colors:
            button = self.create_emoji_button(color)
            flowbox.add(button)

def main(verison):
    window = Smile()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()

    Gtk.main()