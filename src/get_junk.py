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
import requests

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio

class junkGetter():
    def __init__(self, box) -> None:
        self.box = box

    def get_some_junk(self):
        print(hasattr(self, 'list_box'))
        if (hasattr(self, 'list_box')):
            self.box.remove(self.list_box)
            
        self.list_box = Gtk.ListBox()
        self.box.pack_end(self.list_box, True, True, 0)

        spinner = Gtk.Spinner()
        self.list_box.add(spinner)
        spinner.start()

        self.list_box.show_all()

        list = requests.get(url="https://gorest.co.in/public/v1/users").json()

        for user in list['data']:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label = user['email']) 
            
            row.add(label)
            self.list_box.add(row)
            
        spinner.stop()
        self.list_box.show_all()
        