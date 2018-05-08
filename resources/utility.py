# -*- coding: utf-8 -*-


################################################################################
#
# resources/utility.py
# This file contains functions for utility purposes.
#
################################################################################


def expand_mod(mods, count, crit_applied):
    """Expands a modifier list as needed. Ensures len(mods) == count"""

    diff = count - len(mods)
    if diff == 0:
        return mods

    last_value = mods[len(mods) - 1]
    for _ in range(0, diff):
        mods.append(last_value)

    if not crit_applied:
        return mods

    else:
        extended_mods = []
        for mod in mods:
            extended_mods += [mod, mod]

        return extended_mods


def get_weapon(weapon_data, weapon_name, section_name):
    """Gets the weapon data."""

    for section in weapon_data:
        if section["category"] != section_name:
            continue

        for weapon in section["weapons"]:
            if weapon["name"] == weapon_name:
                return weapon
    return None