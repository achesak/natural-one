# -*- coding: utf-8 -*-
from gi.repository import Gio, Gtk


def load_symbolic(name):
    return Gtk.Image.new_from_gicon(
        Gio.ThemedIcon(name='{name}-symbolic'.format(name=name)),
        Gtk.IconSize.BUTTON,
    )
