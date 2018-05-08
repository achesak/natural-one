# -*- coding: utf-8 -*-


################################################################################
#
# resources/launch.py
# This file defines functions for loading application data.
#
################################################################################


# Import necessary modules.
import json
import sys


def get_menu_data():
    """Reads the menu data."""

    try:
        menu_file = open("resources/ui/menu.xml")
        menu_data = menu_file.read()
        menu_file.close()

    except IOError as e:
        print("get_menu_data(): Error reading menu data:\n%s" % e)
        sys.exit()

    return menu_data


def get_weapon_data():
    """Reads and parses the weapon data."""

    try:
        weapon_file = open("resources/data/weapons.json", "r")
        weapon_data = json.load(weapon_file)
        weapon_file.close()

    except (IOError, TypeError, ValueError) as e:
        print("get_weapon_data(): Error reading weapon data:\n%s" % e)
        sys.exit()

    return weapon_data
