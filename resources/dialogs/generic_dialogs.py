# -*- coding: utf-8 -*-


################################################################################
#
# resources/dialogs/generic_dialogs.py
# These are generic dialogs for various purposes.
#
################################################################################


from gi.repository import Gtk


def error(title="", message="", buttons=Gtk.DialogType.OK):
    """Shows an error dialog."""

    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, buttons, title)
    dialog.format_secondary_text(message)
    response = dialog.run()
    dialog.destroy()
    return response


def question(title="", message="", buttons=Gtk.DialogType.OK_CANCEL):
    """Shows a question dialog."""

    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, buttons, title)
    dialog.format_secondary_text(message)
    response = dialog.run()
    dialog.destroy()
    return response