# -*- coding: utf-8 -*-


################################################################################
#
# resources/launch.py
# This file defines functions for loading application data.
#
################################################################################


import json
import sys


def get_menu_data():
    """Reads the menu data."""

    try:
        with open("resources/ui/menu.xml", "r") as menu_file:
            return menu_file.read()
    except IOError as e:
        print("get_menu_data(): Error reading menu data:\n%s" % e)
        sys.exit()


def get_weapon_data():
    """Reads and parses the weapon data."""

    try:
        with open("resources/data/weapons/pathfinder.json", "r") as weapon_file:
            return json.load(weapon_file)
    except (IOError, TypeError, ValueError) as e:
        print("get_weapon_data(): Error reading weapon data:\n%s" % e)
        sys.exit()
