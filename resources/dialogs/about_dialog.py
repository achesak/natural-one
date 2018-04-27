# -*- coding: utf-8 -*-


################################################################################
#
# resources/dialogs/about_dialog.py
# This dialog displays information about the application.
#
################################################################################


# Import Gtk for the dialog.
from gi.repository import Gtk


class NaturalOneAboutDialog(Gtk.AboutDialog):
    """Shows the About dialog."""

    def __init__(self, parent, title, version, icon, license_text):
        """Create the dialog."""

        Gtk.AboutDialog.__init__(self, transient_for=parent)
        self.set_transient_for(parent)

        # Set the details.
        self.set_title("About Natural One")
        self.set_program_name(title)
        self.set_logo(icon)
        self.set_version(version)
        self.set_comments("Natural One is a dice roller designed primarily for the Pathfinder tabletop " +
                          "roll-playing game.")
        self.set_copyright("Copyright (c) 2018 Adam Chesak")
        self.set_authors(["Adam Chesak <achesak@yahoo.com>"])
        self.set_license(license_text)
        self.set_website("https://github.com/achesak/natural-one")
        self.set_website_label("https://github.com/achesak/natural-one")

        # Show the dialog.
        self.show_all()
