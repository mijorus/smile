import os
import gi

from gi.repository import Gtk, Gio, Gdk, GLib, Adw

class UriRow(Adw.ActionRow):
    def __init__(self, website: str, title: str):
        super().__init__()
        self.website = website

        self.set_title(title),
        self.set_selectable(False)

        row_btn = Gtk.Button(icon_name='arrow2-top-right-symbolic', valign=Gtk.Align.CENTER, tooltip_text=_('Open URL'),)
        row_btn.connect('clicked', self.on_web_browser_open_btn_clicked)

        row.connect('changed', self.on_web_browser_input_apply)
        row.add_suffix(row_btn)
    
    def on_web_browser_open_btn_clicked(self):
        Gtk.UriLauncher.new(self.website).launch()