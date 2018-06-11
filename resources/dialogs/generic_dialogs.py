# -*- coding: utf-8 -*-


################################################################################
#
# resources/dialogs/generic_dialogs.py
# These are generic dialogs for various purposes.
#
################################################################################


from gi.repository import Gtk


def error(parent, title="", message="", buttons=Gtk.ButtonsType.OK):
    """Shows an error dialog."""

    dialog = Gtk.MessageDialog(parent, 0, Gtk.MessageType.ERROR, buttons, title)
    dialog.format_secondary_text(message)
    response = dialog.run()
    dialog.destroy()
    return response


def message(parent, title="", message="", buttons=Gtk.ButtonsType.OK):
    """Shows a message dialog."""

    dialog = Gtk.MessageDialog(parent, 0, Gtk.MessageType.INFO, buttons, title)
    dialog.format_secondary_text(message)
    response = dialog.run()
    dialog.destroy()
    return response


def question(parent, title="", message="", buttons=Gtk.ButtonsType.OK_CANCEL):
    """Shows a question dialog."""

    dialog = Gtk.MessageDialog(parent, 0, Gtk.MessageType.QUESTION, buttons, title)
    dialog.format_secondary_text(message)
    response = dialog.run()
    dialog.destroy()
    return response