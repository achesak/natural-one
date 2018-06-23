# -*- coding: utf-8 -*-
from gi.repository import Gtk


def show_error(parent, title='', message='', buttons=None):
    dialog = Gtk.MessageDialog(
        parent,
        0,
        Gtk.MessageType.ERROR,
        buttons or Gtk.ButtonsType.OK,
        title,
    )
    dialog.format_secondary_text(message)
    response = dialog.run()
    dialog.destroy()
    return response


def show_message(parent, title='', message='', buttons=None):
    dialog = Gtk.MessageDialog(
        parent,
        0,
        Gtk.MessageType.INFO,
        buttons or Gtk.ButtonsType.OK,
        title,
    )
    dialog.format_secondary_text(message)
    response = dialog.run()
    dialog.destroy()
    return response


def show_question(parent, title='', message='', buttons=None):
    dialog = Gtk.MessageDialog(
        parent,
        0,
        Gtk.MessageType.QUESTION,
        buttons or Gtk.ButtonsType.OK_CANCEL,
        title,
    )
    dialog.format_secondary_text(message)
    response = dialog.run()
    dialog.destroy()
    return response == Gtk.ResponseType.OK
