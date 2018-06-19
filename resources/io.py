# -*- coding: utf-8 -*-
import json
import os
import platform
import shutil
import sys

import resources.launch as launch


def get_main_dir():
    """Returns the main directory."""

    # Windows support here for future full implementation.
    if platform.system().lower() == "windows":
        path = os.environ["LOCALAPPDATA"] + "\\naturalone"
    else:
        path = os.path.expanduser("~") + "/.local/share/naturalone"

    if not os.path.exists(path):
        os.makedirs(path)

    return path


def get_systems_dir():
    """Returns the systems directory."""

    root_path = get_main_dir()
    systems_path = os.path.join(root_path, "systems")

    if not os.path.exists(systems_path):
        os.makedirs(systems_path)

    return systems_path


def get_systems_settings_path():
    """Returns the path to the systems settings file."""

    root_path = get_main_dir()
    return os.path.join(root_path, "systems.json")


def create_systems_settings():
    """Copies default systems settings to user data."""

    try:
        shutil.copyfile("resources/data/weapons.json", get_systems_settings_path())
    except IOError:
        print("IOError copying systems settings")
        sys.exit()


def load_systems_settings():
    """Loads the systems settings."""

    with open(get_systems_settings_path(), "a+") as systems_file:
        systems_file.seek(0)
        try:
            return json.load(systems_file)
        except (IOError, TypeError, ValueError):
            create_systems_settings()
            return load_systems_settings()


def save_systems_settings(systems):
    """Saves the systems settings."""

    try:
        with open(get_systems_settings_path(), "w") as systems_file:
            json.dump(systems, systems_file)
    except IOError:
        print("IOError saving systems")


def get_template_path():
    """Returns the path to the template file."""

    root_path = get_main_dir()
    return os.path.join(root_path, "templates.json")


def load_templates():
    """Loads the templates."""

    with open(get_template_path(), "a+") as template_file:
        template_file.seek(0)
        try:
            return json.load(template_file)
        except (IOError, TypeError, ValueError):
            template_file.write("[]")
            return []


def save_templates(templates):
    """Saves the templates."""

    write_templates(get_template_path(), templates)


def read_templates(filename):
    """Reads the templates from a file."""

    with open(filename, "r") as template_file:
        try:
            return json.load(template_file)
        except (IOError, TypeError, ValueError):
            print("Error reading templates")


def write_templates(filename, templates):
    """Writes the templates to a file."""

    try:
        with open(filename, "w") as template_file:
            json.dump(templates, template_file)
    except IOError:
        print("IOError writing templates")
