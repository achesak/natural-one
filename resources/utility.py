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
