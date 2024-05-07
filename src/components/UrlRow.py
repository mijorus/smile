import gi

from gi.repository import Gtk, Gio, Gdk, GLib, Adw

class UriRow(Adw.ActionRow):
    def __init__(self, website: str, title: str, subtitle=False):
        super().__init__()
        self.website = website
        
        self.set_title(title)
        if subtitle:
            self.set_subtitle(subtitle)

        self.set_selectable(False)

        row_btn = Gtk.Button(icon_name='arrow2-top-right-symbolic', valign=Gtk.Align.CENTER)
        row_btn.connect('clicked', self.on_web_browser_open_btn_clicked)

        self.add_suffix(row_btn)
    
    def on_web_browser_open_btn_clicked(self, *args):
        Gtk.UriLauncher.new(self.website).launch()