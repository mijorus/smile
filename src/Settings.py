import manimpango
import sys
import gi
from .assets.emoji_list import emojis
from .lib.custom_tags import set_custom_tags, get_custom_tags, get_all_custom_tags, delete_custom_tags


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GLib

class Settings():
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_resource('/it/mijorus/smile/ui/settings.glade')
        self.window = builder.get_object('settings-window')
        
        self.list_box = builder.get_object('preferencies-listbox')
        self.custom_tags_list_box = builder.get_object('customtags-listbox')
        self.empty_list_label = Gtk.Label(label="There are no custom tags for any emoji yet; create one with <b>Alt+T</b>", use_markup=True, margin=10)

        self.settings = Gio.Settings.new('it.mijorus.smile')
        self.create_boolean_settings_entry('Open on mouse position', 'open-on-mouse-position', 'Might not work on Wayland systems')
        self.create_custom_tags_list()
        self.custom_tags_entries: list[Gtk.Entry] = []
        self.window.connect('destroy', self.on_window_close)

        self.window.show_all()

    def create_boolean_settings_entry(self, label: str, key: str, subtitle: str = None):
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, margin=10)
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, expand=True, margin=0, can_focus=False)
        switch = Gtk.Switch()

        box.pack_start(Gtk.Label(label=label, halign=Gtk.Align.START), True, True, 0)
        box.pack_end(switch, False, False, 0)

        container.pack_start(box, False,False, 0)
        
        self.settings.bind(key, switch, 'state', Gio.SettingsBindFlags.DEFAULT)

        if subtitle:
            container.pack_end(Gtk.Label(label=f"<small>{subtitle}</small>", halign=Gtk.Align.START, use_markup=True), False, False, 0)

        listbox_row = Gtk.ListBoxRow(selectable=False)
        listbox_row.add(container)
        self.list_box.add(listbox_row)

    def create_custom_tags_list(self):
        custom_tags = get_all_custom_tags()

        rows = []
        if not len(custom_tags):
            rows.append(self.empty_list_label)
        else:
            for hexcode, tags in custom_tags.items():
                box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, expand=True, margin=5)
                
                for e, data in emojis.items():
                    if (e == hexcode):
                        label = Gtk.Label(label=data['emoji'], halign=Gtk.Align.START)
                        label.get_style_context().add_class('emoji_with_custom_tags_preferencies')
                        box.pack_start( label, False, True,  5 )

                        delete_button = Gtk.Button(label="Remove")
                        delete_button.get_style_context().add_class('destructive-action')
                        delete_button.connect('clicked', lambda w: self.delete_tag(e))

                        box.pack_end(delete_button, False, True,  5)

                        entry = Gtk.Entry(text=tags['tags'])
                        entry.hexcode = hexcode
                        
                        box.pack_end(entry, True, True, 5 )
                        box.hexcode = e

                        break

                rows.append(box)

        
        for row in rows:
            listbox_row = Gtk.ListBoxRow(selectable=False)
            listbox_row.add(row)
            self.custom_tags_list_box.add(listbox_row)

    def delete_tag(self, hexcode: str):
        result = delete_custom_tags(hexcode)

        if result:
            for child in self.custom_tags_list_box.get_children():
                if child.get_children()[0].hexcode == hexcode:
                    child.destroy()
                    break

        if (not get_all_custom_tags()) or (len(get_all_custom_tags()) == 0):
            listbox_row = Gtk.ListBoxRow(selectable=False, visible=True)
            listbox_row.add(self.empty_list_label)
            self.custom_tags_list_box.add(listbox_row)
            self.custom_tags_list_box.show_all()

    def on_window_close(self, widget: Gtk.Window):
        for listbox_row in self.custom_tags_list_box.get_children():
            row = listbox_row.get_children()[0]
             
            for widget in row:
                if isinstance(widget, Gtk.Entry):
                    set_custom_tags(row.hexcode, widget.get_text())
                    break
