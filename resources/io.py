# -*- coding: utf-8 -*-


################################################################################
#
# resources/io.py
# This file defines functions for saving and loading user data.
#
################################################################################


# Import necessary modules.
import json
import sys
import os
import platform


def get_main_dir():
    """Returns the main directory."""

    # Windows:
    # * Data: C:\Users\[username]\AppData\Local\naturalone
    # Linux:
    # * Data: /home/[username]/.share/local/naturalone
    # OSX: probably the same as Linux?
    path = None
    if platform.system().lower() == "windows":
        path = os.environ["LOCALAPPDATA"] + "\\naturalone"
    else:
        path = os.path.expanduser("~") + "/.local/share/naturalone"

    # Create if necessary.
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def load_templates():
    """Loads the templates."""

    root_path = get_main_dir()
    path = os.path.join(root_path, "templates.json")

    try:
        template_file = open(path, "r")
        templates = json.load(template_file)
        template_file.close()

    except IOError:
        template_file = open(path, "w")
        template_file.write("[]")
        template_file.close()
        templates = []

    return templates


def save_templates(templates):
    """Saves the templates."""

    root_path = get_main_dir()
    path = os.path.join(root_path, "templates.json")

    try:
        template_file = open(path, "w")
        json.dump(templates, template_file)
        template_file.close()

    except IOError:
        print("IOError saving templates")

