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

from gi.repository import Gtk, Gio

class Handler:
    def onButtonPressed(self, button):
        print("Hello World!")
        label = builder.get_object('label')
        label.set_label('pressed!')

    def onHandleMove(self, el):
        print("Hello World!")
        builder.get_object('label').set_label('move!')


builder = Gtk.Builder()
builder.add_from_file("src/window.glade")
builder.connect_signals(Handler())

def main(verison):
    window = builder.get_object("window")
    window.connect("destroy", Gtk.main_quit)
    window.show_all()

    Gtk.main()