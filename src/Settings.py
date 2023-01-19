import gi
import dbus
import time

from dbus.mainloop.glib import DBusGMainLoop
from .assets.emoji_list import emojis
from .lib.custom_tags import set_custom_tags, get_all_custom_tags, delete_custom_tags
from .lib.localized_tags import get_countries_list
from .utils import read_text_resource, is_wayland


from gi.repository import Gtk, Gio, Gdk, GLib, Adw


class Settings(Adw.PreferencesWindow):
    def __init__(self, application_id: str):
        super().__init__()
        self.application_id = application_id
        self.settings = Gio.Settings.new('it.mijorus.smile')

        self.page1 = Adw.PreferencesPage(title='Settings', icon_name='settings-symbolic')
        general_group = Adw.PreferencesGroup(title='General')
        general_group.add(
            self.create_boolean_settings_entry('Run in the background', 'load-hidden-on-startup', 'Keep Smile running in the background for a faster launch')
        )

        general_group.add(
            self.create_boolean_settings_entry('Minimize on exit', 'iconify-on-esc',  'Minimize the window when selecting an emoji')
        )

        general_group.add(self.create_launch_shortcut_settings_entry())

        customization_group = Adw.PreferencesGroup(title='Customization')
        customization_group.add(self.create_modifiers_combo_boxes())

        self.localized_tags_group = Adw.PreferencesGroup(title='Localized tags')
        self.localized_tags_group.add(
            self.create_boolean_settings_entry('Use localized tags', 'use-localized-tags', '',)
        )

        self.localized_tags_group.add(
            self.create_boolean_settings_entry(
                'Merge localized and English tags',
                'merge-english-tags',
                'Use both localized tags and English ones at the same time'
            )
        )

        self.localized_tags_group.add(self.create_tags_locale_combo_boxes())

        self.page1.add(general_group)
        self.page1.add(customization_group)
        self.page1.add(self.localized_tags_group)

        self.page2 = Adw.PreferencesPage(title='Custom tags', icon_name='smile-symbolic')
        self.custom_tags_list_box = Gtk.ListBox(css_classes=['boxed-list'])

        self.custom_tags_rows = self.create_custom_tags_list()
        for row in self.custom_tags_rows:
            self.custom_tags_list_box.append(row)

        self.custom_tags_group = Adw.PreferencesGroup()
        self.custom_tags_group.add(self.custom_tags_list_box)
        self.page2.add(self.custom_tags_group)

        self.add(self.page1)
        self.add(self.page2)

        if not self.settings.get_boolean('use-localized-tags'):
            self.localized_tags_group.set_opacity(0.7)

        self.custom_tags_entries: list[Gtk.Entry] = []
        self.settings.connect('changed', self.on_settings_changes)
        self.connect('close-request', self.on_window_close)

        self.present()

    def create_boolean_settings_entry(self, label: str, key: str, subtitle: str = None, usable: bool = True, add_to=None) -> Adw.ActionRow:
        row = Adw.ActionRow(title=label, subtitle=subtitle)

        switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        self.settings.bind(key, switch, 'state', Gio.SettingsBindFlags.DEFAULT)

        row.add_suffix(switch)
        return row

    def create_launch_shortcut_settings_entry(self) -> Adw.ActionRow:
        row = Adw.ActionRow(
            title='Launch the app with a shortcut',
            subtitle='Create a new keyboard shortcut in your system settings and paste the following code as a custom command'
        )

        row.add_suffix(Gtk.Label(label=f'flatpak run {self.application_id}', selectable=True))

        return row

    def create_custom_tags_list(self) -> list:
        custom_tags = get_all_custom_tags()

        rows = []
        if not len(custom_tags):
            rows.append(self.empty_list_label)
        else:
            for hexcode, config in custom_tags.items():
                if not 'tags' in config or not config['tags']:
                    continue

                listbox_row = Gtk.ListBoxRow(selectable=False)

                box = Gtk.Box(
                    spacing=10,
                    halign=Gtk.Align.CENTER,
                    orientation=Gtk.Orientation.HORIZONTAL,
                    margin_top=10,
                    margin_bottom=10,
                    margin_start=5,
                    margin_end=5,
                )

                for e, data in emojis.items():
                    if (e == hexcode):
                        label = Gtk.Label(label=data['emoji'], halign=Gtk.Align.START, css_classes=['title-2'])
                        box.append(label)

                        entry = Gtk.Entry(text=config['tags'], width_chars=35)
                        entry.hexcode = hexcode
                        box.append(entry)

                        delete_button = Gtk.Button(label="Remove", css_classes=['destructive-action'])
                        delete_button.hexcode = e
                        delete_button.connect('clicked', lambda w: self.delete_tag(w.hexcode))

                        box.append(delete_button)

                        listbox_row.__entry = entry
                        listbox_row.hexcode = hexcode

                        listbox_row.set_child(box)
                        rows.append(listbox_row)

                        break

        return rows

    def delete_tag(self, hexcode: str):
        for r in self.custom_tags_rows:
            self.custom_tags_list_box.remove(r)

        if delete_custom_tags(hexcode):
            self.custom_tags_rows = self.create_custom_tags_list()
            for row in self.custom_tags_rows:
                self.custom_tags_list_box.append(row)

    def create_error_dialog(self, text: str):
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=text,
        )

        dialog.run()
        dialog.destroy()

    def create_modifiers_combo_boxes(self) -> Adw.ActionRow:
        row = Adw.ActionRow(title='Default skintone')
        skintones = [["", "👋"], ["1F3FB", "👋🏻"], ["1F3FC", "👋🏼"], ["1F3FD", "👋🏽"], ["1F3FE", "👋🏾"], ["1F3FF", "👋🏿"]]
        skintones_combo = Gtk.ComboBoxText(valign=Gtk.Align.CENTER)

        for i, j in enumerate(skintones):
            skintones_combo.append(j[0], j[1])

            if self.settings.get_string('skintone-modifier') == j[0]:
                skintones_combo.set_active(i)

        skintones_combo.connect('changed', lambda w: self.settings.set_string('skintone-modifier', w.get_active_id()))
        row.add_suffix(skintones_combo)
        return row

    def create_tags_locale_combo_boxes(self) -> Adw.ActionRow:
        row = Adw.ActionRow(title='Localized tags')
        locales_combo = Gtk.ComboBoxText(valign=Gtk.Align.CENTER)

        i = 0
        for k, v in get_countries_list().items():
            locales_combo.append(k, v['flag'] + ' ' + k.upper())

            if self.settings.get_string('tags-locale') == k:
                locales_combo.set_active(i)

            i += 1

        locales_combo.connect('changed', lambda w: self.settings.set_string('tags-locale', w.get_active_id()))
        row.add_suffix(locales_combo)
        return row

    def on_settings_changes(self, settings, key: str):
        callback = getattr(self, f"on_{key.replace('-', '_')}_changed", None)

        if callback:
            callback(settings, key)

    def on_window_close(self, widget: Gtk.Window):
        for row in self.custom_tags_rows:
            set_custom_tags(row.hexcode, row.__entry.get_text())

    def on_use_localized_tags_changed(self, settings, key: str):
        if settings.get_boolean(key):
            self.localized_tags_group.set_opacity(1)
        else:
            self.localized_tags_group.set_opacity(0.7)

    def on_load_hidden_on_startup_changed(self, settings, key: str):
        value: bool = settings.get_boolean(key)

        old_autostart_file = Gio.File.new_for_path(f'{GLib.get_home_dir()}/.config/autostart/smile.autostart.desktop')
        if old_autostart_file.query_exists():
            old_autostart_file.delete()

        bus = dbus.SessionBus()
        obj = bus.get_object("org.freedesktop.portal.Desktop", "/org/freedesktop/portal/desktop")
        inter = dbus.Interface(obj, "org.freedesktop.portal.Background")
        res = inter.RequestBackground('', {'reason': 'Smile autostart', 'autostart': value, 'background': value, 'commandline': dbus.Array(['smile', '--start-hidden'])})
