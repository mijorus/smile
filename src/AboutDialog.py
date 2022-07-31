from gi.repository import Gtk

class AboutDialog(Gtk.AboutDialog):
    def __init__(self, parent, **kwargs):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'Smile'
        self.props.version = kwargs['version']
        self.props.website = 'https://smile.mijorus.it'
        self.props.authors = ['Lorenzo Paderi']
        self.props.copyright = '(C) 2022 Lorenzo Paderi\nLocalized tags by milesj/emojibase,\nlicensed under the MIT License'
        self.props.logo_icon_name = 'it.mijorus.smile'
        self.set_transient_for(parent)