# -*- coding: utf-8 -*-


################################################################################
#
# resources/utility.py
# This file contains functions for utility purposes.
#
################################################################################


def expand_mod(mods, count, crit_applied):
    """Expands a modifier list as needed. Ensures len(mods) == count"""

    if len(mods) > count:
        del mods[count:]
    else:
        mods.extend([mods[-1]] * (count - len(mods)))

    if crit_applied:
        return [mod for mod in mods for _ in (0, 1)]
    else:
        return mods


def get_weapon(weapon_data, weapon_name, section_name):
    """Gets the weapon data."""

    section_elem = (section for section in weapon_data if section["category"] == section_name).next()
    weapon_elem = (weapon for weapon in section_elem["weapons"] if weapon["name"] == weapon_name).next()
    return weapon_elem
