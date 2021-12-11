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

from .get_junk import junkGetter

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio

class Handler():
    j = None

    def onJunkRequested(self, widget):
        if not self.j:
            self.j = junkGetter(builder.get_object('list-container'))

        self.j.get_some_junk()


    # def onSubtract(self, button):
    #     self.counter -= 1
    #     builder.get_object('label').set_label(str(self.counter))


builder = Gtk.Builder()
builder.add_from_file("src/window.glade")
builder.connect_signals(Handler())

def main(verison):
    window = builder.get_object("window")
    window.connect("destroy", Gtk.main_quit)
    window.show_all()

    Gtk.main()