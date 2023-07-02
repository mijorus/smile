import dbus
from gi.repository import GLib, Gio

_tags_cache = {}
def tag_list_contains(tags: str, q: str) -> bool:
    global _tags_cache

    q = q.lower()

    if tags in _tags_cache:
        tags_arr = _tags_cache[tags]
    else:
        tags_arr = tags.replace(', ', ',').split(',')
        _tags_cache[tags] = tags_arr

    for t in tags_arr:
        if t.lower().startswith(q):
            return True
    
    return False

# thank you mate ❤️
# https://github.com/gtimelog/gtimelog/blob/6e4b07b58c730777dbdb00b3b85291139f8b10aa/src/gtimelog/main.py#L159
def make_option(long_name, short_name=None, flags=0, arg=GLib.OptionArg.NONE, arg_data=None, description=None, arg_description=None):
    # surely something like this should exist inside PyGObject itself?!
    option = GLib.OptionEntry()
    option.long_name = long_name.lstrip('-')
    option.short_name = 0 if not short_name else short_name.lstrip('-')
    option.flags = flags
    option.arg = arg
    option.arg_data = arg_data
    option.description = description
    option.arg_description = arg_description
    return option

def read_text_resource(res: str) -> str:
    file = Gio.resources_lookup_data(res, Gio.ResourceLookupFlags.NONE)
    data: bytes = file.get_data()

    decoded = data.decode('utf-8')
    file.unref()
    return decoded

def portal(interface: str, bus_name: str='org.freedesktop.portal.Desktop', object_path: str='/org/freedesktop/portal/desktop') -> dbus.Interface:
    bus = dbus.SessionBus()
    obj = bus.get_object(bus_name, object_path)
    inter = dbus.Interface(obj, interface)

    return inter