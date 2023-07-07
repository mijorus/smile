import os
import gi
import json
from datetime import datetime

from dbus import Array as DBusArray
from .assets.emoji_list import emojis
from .lib.user_config import read_json_config, save_json_config
from .lib.custom_tags import set_custom_tags, get_all_custom_tags, delete_custom_tags
from .lib.localized_tags import get_countries_list
from .utils import portal
from .components.UrlRow import UriRow
from .lib.DbusService import DbusService, GNOME_EXTENSION_LINK


from gi.repository import Gtk, Gio, Gdk, GLib, Adw


class Settings(Adw.PreferencesWindow):
    def __init__(self, application_id: str, **kwargs):
        super().__init__(**kwargs)
        self.application_id = application_id
        self.settings = Gio.Settings.new('it.mijorus.smile')

        if self.settings.get_string('tags-locale') == 'en':
            self.settings.set_string('tags-locale', 'da')

        self.page1 = Adw.PreferencesPage(title=_('Settings'), icon_name='smile-settings-symbolic')
        general_group = Adw.PreferencesGroup(title=_('General'))
        general_group.add(
            self.create_boolean_settings_entry(_('Run in the background'), 'load-hidden-on-startup', _('Keep Smile running in the background for a faster launch'))
        )

        general_group.add(
            self.create_boolean_settings_entry(_('Minimize on exit'), 'iconify-on-esc',  _('Minimize the window when selecting an emoji'))
        )

        general_group.add(self.create_launch_shortcut_settings_entry())

        paste_emoji_group = Adw.PreferencesGroup(title=_('Paste emojis automatically'))
        
        auto_paste_status = self.get_autopaste_status()
        auto_paste_suff = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3, valign=Gtk.Align.CENTER, tooltip_text=auto_paste_status[3])
    
        [auto_paste_suff.append(el) for el in [
            Gtk.Label(label=_('Status:'), css_classes=['heading']), 
            Gtk.Image(icon_name=auto_paste_status[1], css_classes=[auto_paste_status[2]])
        ]]

        use_ext_row =  self.create_boolean_settings_entry(
            _('Enabled'), 
            'auto-paste',
            _('Emulates the Ctrl+V shortcut; might <b>not work</b> on some programs.\nIf using the extension, <b>please ensure that it is correctly ENABLED</b>.')
        )

        paste_emoji_group.set_header_suffix(auto_paste_suff)
        use_ext_row.set_sensitive(auto_paste_status[0])

        get_ext_link_row = UriRow(website=GNOME_EXTENSION_LINK, title=_('Get the GNOME extension'), subtitle=_('Install the extension to paste automatically on X11 and Wayland'))
        [paste_emoji_group.add(el) for el in [use_ext_row, get_ext_link_row]]

        customization_group = Adw.PreferencesGroup(title=_('Customization'))
        customization_group.add(self.create_modifiers_combo_boxes())
        customization_group.add(self.create_emoji_sizes_combo_boxes())

        self.localized_tags_group = Adw.PreferencesGroup(title=_('Localized tags'))
        self.localized_tags_group.add(
            self.create_boolean_settings_entry(_('Use localized tags'), 'use-localized-tags', '',)
        )

        self.localized_tags_group_items = [
            self.create_boolean_settings_entry(
                _('Merge localized and English tags'),
                'merge-english-tags',
                _('Use both localized tags and English ones at the same time')
            ),
            self.create_tags_locale_combo_boxes()
        ]

        [self.localized_tags_group.add(item) for item in self.localized_tags_group_items]
        [self.page1.add(el) for el in [general_group, paste_emoji_group, customization_group, self.localized_tags_group]]

        # Page 2

        self.page2 = Adw.PreferencesPage(title=_('Custom tags'), icon_name='smile-symbolic')
        self.custom_tags_list_box = Gtk.ListBox(css_classes=['boxed-list'])
        
        bldr = Gtk.Builder()
        bldr.add_from_resource('/it/mijorus/smile/ui/importexport-customtags.ui')
        import_export_widget = bldr.get_object('importexport_group')

        bldr.get_object('importexport_export_button').connect('clicked', self.on_export_tags_clicked)
        bldr.get_object('importexport_import_button').connect('clicked', self.on_import_tags_clicked)
        self.page2.add(import_export_widget)

        self.custom_tags_rows = self.create_custom_tags_list()
        [self.custom_tags_list_box.append(row) for row in self.custom_tags_rows]

        self.custom_tags_group = Adw.PreferencesGroup()
        self.custom_tags_group.add(self.custom_tags_list_box)
        self.page2.add(self.custom_tags_group)


        self.add(self.page1)
        self.add(self.page2)

        self.on_use_localized_tags_changed(self.settings, 'use-localized-tags')

        self.custom_tags_entries: list[Gtk.Entry] = []
        self.settings.connect('changed', self.on_settings_changes)
        self.connect('close-request', self.on_window_close)

    def get_autopaste_status(self):
        if DbusService.extension_status == 'installed':
            return (True, 'checkmark-symbolic', 'success', _('Available (using the GNOME extension)'))
        elif os.getenv('XDG_SESSION_TYPE') == 'wayland':
            return (False, 'warning-small-symbolic', 'warning', _('Requires the GNOME extension on Wayland'))
        else:
            return (True, 'checkmark-symbolic', 'success', _('Available (using xdotool on X11)'))

    def create_boolean_settings_entry(self, label: str, key: str, subtitle: str = None, usable: bool = True, add_to=None) -> Adw.ActionRow:
        row = Adw.ActionRow(title=label, subtitle=subtitle)

        switch = Gtk.Switch(valign=Gtk.Align.CENTER)
        self.settings.bind(key, switch, 'active', Gio.SettingsBindFlags.DEFAULT)

        row.add_suffix(switch)
        return row

    def create_launch_shortcut_settings_entry(self) -> Adw.ActionRow:
        row = Adw.ActionRow(
            title=_('Launch the app with a shortcut'),
            subtitle=_('Create a new keyboard shortcut in your system settings and paste the following code as a custom command')
        )

        row.add_suffix(Gtk.Label(label=f'flatpak run {self.application_id}', selectable=True))

        return row

    def create_custom_tags_list(self) -> list:
        custom_tags = get_all_custom_tags()

        rows = []
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

                    delete_button = Gtk.Button(label=_("Remove"), css_classes=['destructive-action'])
                    delete_button.hexcode = e
                    delete_button.connect('clicked', lambda w: self.delete_tag(w.hexcode))

                    box.append(delete_button)

                    listbox_row.__entry = entry
                    listbox_row.hexcode = hexcode

                    listbox_row.set_child(box)
                    rows.append(listbox_row)

                    break

        if not rows:
            rows.append(
                Adw.ActionRow(title=_("There are no custom tags yet: create one with Alt + T"))
            )

        return rows

    def delete_tag(self, hexcode: str):
        [self.custom_tags_list_box.remove(r) for r in self.custom_tags_rows]

        if delete_custom_tags(hexcode):
            self.custom_tags_rows = self.create_custom_tags_list()
            [self.custom_tags_list_box.append(row) for row in self.custom_tags_rows]

    def create_modifiers_combo_boxes(self) -> Adw.ActionRow:
        row = Adw.ActionRow(title=_('Default skintone'))
        skintones = [["", "👋"], ["1F3FB", "👋🏻"], ["1F3FC", "👋🏼"], ["1F3FD", "👋🏽"], ["1F3FE", "👋🏾"], ["1F3FF", "👋🏿"]]
        skintones_combo = Gtk.ComboBoxText(valign=Gtk.Align.CENTER)

        for i, j in enumerate(skintones):
            skintones_combo.append(j[0], j[1])

            if self.settings.get_string('skintone-modifier') == j[0]:
                skintones_combo.set_active(i)

        skintones_combo.connect('changed', lambda w: self.settings.set_string('skintone-modifier', w.get_active_id()))
        row.add_suffix(skintones_combo)
        return row
    
    def create_emoji_sizes_combo_boxes(self) -> Adw.ActionRow:
        row = Adw.ActionRow(title=_('Emoji size'))
        sizes = [
            [_("Default"), "emoji-button"], 
            [_("Big"), "emoji-button-lg"], 
            [_("Bigger"), "emoji-button-xl"],
            [_("Giant"), "emoji-button-xxl"]
        ]

        emoji_size_combo = Gtk.ComboBoxText(valign=Gtk.Align.CENTER)

        for i, j in enumerate(sizes):
            emoji_size_combo.append(j[1], j[0])

            if self.settings.get_string('emoji-size-class') == j[1]:
                emoji_size_combo.set_active(i)

        emoji_size_combo.connect('changed', lambda w: self.settings.set_string('emoji-size-class', w.get_active_id()))
        row.add_suffix(emoji_size_combo)
        return row

    def create_tags_locale_combo_boxes(self) -> Adw.ActionRow:
        row = Adw.ActionRow(title=_('Localized tags'))
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
            if hasattr(row, 'hexcode'):
                set_custom_tags(row.hexcode, row.__entry.get_text())

    def on_use_localized_tags_changed(self, settings, key: str):
        [item.set_sensitive(settings.get_boolean(key)) for item in self.localized_tags_group_items]

    def on_load_hidden_on_startup_changed(self, settings, key: str):
        value: bool = settings.get_boolean(key)

        old_autostart_file = Gio.File.new_for_path(f'{GLib.get_home_dir()}/.config/autostart/smile.autostart.desktop')
        if old_autostart_file.query_exists():
            old_autostart_file.delete()

        inter = portal("org.freedesktop.portal.Background")
        res = inter.RequestBackground('', {'reason': 'Smile autostart', 'autostart': value, 'background': value, 'commandline': DBusArray(['smile', '--start-hidden'])})

    def on_export_tags_clicked(self, w):
        dialog = Gtk.FileDialog()
        dialog.set_initial_name('smile-tag-export-' + datetime.now().strftime('%Y-%m-%d-%H%M') + '.json')
        dialog.save(self, None, self.on_export_tags_done)

    def on_import_tags_clicked(self, w):
        dialog = Gtk.FileDialog()
        dialog.open(self, None, self.on_import_tags_done)

    def on_export_tags_done(self, source, res):
        try:
            filename = res.get_source_object().save_finish(res).get_path()

            with open(filename, 'w+') as f:
                f.write(json.dumps(read_json_config('custom_tags')))
        except Exception as e:
            print(e)

    def on_import_tags_done(self, source, res):
        try:
            filename = res.get_source_object().open_finish(res).get_path()
        except Exception as e:
            return print(e)

        try:
            with open(filename, 'r') as f:
                restore = json.loads(f.read())

                if isinstance(restore, dict) and any(em in emojis.keys() for em in restore.keys()):
                    print('Restoring from backup...')
                    save_json_config(restore, 'custom_tags')

                    [self.custom_tags_list_box.remove(r) for r in self.custom_tags_rows]

                    self.custom_tags_rows = self.create_custom_tags_list()
                    [self.custom_tags_list_box.append(row) for row in self.custom_tags_rows]
                else:
                    raise Exception('Invalid restore file')
        except Exception as e:
            print(e)

            dialog = Adw.MessageDialog.new(
                self,
                _('Invalid file selected'),
                _('The configuration file that you selected is not a valid backup.'),
            )

            dialog.add_response('close', _('Close'))
            dialog.set_close_response('close')
            dialog.present()