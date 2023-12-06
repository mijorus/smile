import gi

gi.require_version('Gtk', '4.0')

from gi.repository import Gtk, Gio, Gdk  # noqa

FLOWBOX_CHILD_DEFAULT_CSS = ['flowbox-child-custom']

def create_flowbox_child(emoji_button: Gtk.Button, secondary_click_geture_callback=None, middle_click_gesture_callback=None) -> Gtk.FlowBoxChild:
    flowbox_child = Gtk.FlowBoxChild(child=emoji_button)
    flowbox_child._is_selected = False
    flowbox_child.set_css_classes(FLOWBOX_CHILD_DEFAULT_CSS)

    event_controller_focus = Gtk.EventControllerFocus()
    flowbox_child.add_controller(event_controller_focus)

    event_controller_focus.connect('enter', flowbox_child_on_selection_enter)
    event_controller_focus.connect('leave', flowbox_child_on_selection_leave)

    if secondary_click_geture_callback:
        gesture = Gtk.GestureSingle(button=Gdk.BUTTON_SECONDARY)
        gesture.connect('end', secondary_click_geture_callback)
        flowbox_child.add_controller(gesture)

    if middle_click_gesture_callback:
        gesture_mid_click = Gtk.GestureSingle(button=Gdk.BUTTON_MIDDLE)
        gesture_mid_click.connect('end', middle_click_gesture_callback)
        flowbox_child.add_controller(gesture_mid_click)

    return flowbox_child


def create_emoji_button(emoji_data: dict, click_handler=None) -> Gtk.Button:
    emoji_button = Gtk.Button(label=emoji_data['emoji'])
    emoji_button.emoji_data = emoji_data
    emoji_button.hexcode = emoji_data['hexcode']
    emoji_button.base_skintone_widget = None

    if click_handler:
        emoji_button.connect('clicked', click_handler)

    return emoji_button


def flowbox_child_on_selection_enter(controller, widget=None):
    if not widget:
        widget = controller.get_widget()
    
    widget.set_css_classes(FLOWBOX_CHILD_DEFAULT_CSS)


def flowbox_child_on_selection_leave(controller, widget=None):
    if not widget:
        widget = controller.get_widget()

    if widget._is_selected:
        flowbox_child_set_as_selected(None, widget)
    else:
        flowbox_child_deselect(widget)


def flowbox_child_set_as_selected(controller, widget=None):
    if not widget:
        widget = controller.get_widget()

    widget._is_selected = True
    widget.set_css_classes([*FLOWBOX_CHILD_DEFAULT_CSS, 'selected'])


def flowbox_child_set_as_active(widget: Gtk.FlowBoxChild):
    widget.set_css_classes([*FLOWBOX_CHILD_DEFAULT_CSS, 'active'])


def flowbox_child_deselect(widget: Gtk.FlowBoxChild):
    widget._is_selected = False
    widget.set_css_classes([*FLOWBOX_CHILD_DEFAULT_CSS])


def emoji_button_update_css_classes(widget: Gtk.Button, emoji_size_class):
    emoji_button_css = [emoji_size_class]

    if ('skintones' in widget.emoji_data) and widget.emoji_data['skintones']:
        emoji_button_css.append('emoji-with-skintones')
        
    widget.set_css_classes(emoji_button_css)