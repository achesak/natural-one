# Import json for loading the data files.
import json
import sys


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
