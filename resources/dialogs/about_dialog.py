# -*- coding: utf-8 -*-
from gi.repository import Gtk


class NaturalOneAboutDialog(Gtk.AboutDialog):

    def __init__(self, parent, icon):

        Gtk.AboutDialog.__init__(self, transient_for=parent)
        self.set_transient_for(parent)

        self.set_title('About Natural One')
        self.set_program_name('Natural One')
        self.set_logo(icon)
        self.set_version('1.5')
        self.set_comments('Natural One is a dice roller designed primarily '
                          'for the Pathfinder tabletop roll-playing game.')
        self.set_copyright('© 2018 Adam Chesak')
        self.set_authors(['Adam Chesak <achesak@yahoo.com>'])
        self.set_license_type(Gtk.License.GPL_3_0)
        self.set_website('https://github.com/achesak/natural-one')
        self.set_website_label('https://github.com/achesak/natural-one')

        self.show_all()
