# -*- coding: utf-8 -*-


################################################################################
#
# resources/roller.py
# This file contains functions for generating random dice rolls.
#
################################################################################


import random


def basic(count, die, mod_each, mod_once, min_value):
    """Rolls dice."""

    rolls = []
    total = 0
    for _ in range(0, count):
        roll = random.randint(1, die)
        rolls.append(roll)
        if mod_each:
            roll += mod_each
        roll = max(roll, min_value)
        total += roll
    total += mod_once
    total = max(total, min_value)

    return total, rolls


def atk(num_atks, mods, crit_range, stop_on_crit, confirm_crit):
    """Rolls an attack roll."""

    rolls = []
    for i in range(0, num_atks):
        roll = random.randint(1, 20)
        rolls.append("Attack %d: %d+%d=<b>%d</b>" % (i + 1, roll, mods[i], roll + mods[i]))
        if roll == 1:
            rolls.append("<span color=\"red\">Critical fail!</span>")
            if stop_on_crit:
                break
        if roll >= crit_range:
            rolls.append("<span color=\"green\">Critical hit!</span>")
            if confirm_crit:
                confirm = random.randint(1, 20)
                rolls.append("Critical confirm: %d+%d=<b>%d</b>" % (confirm, mods[i], confirm + mods[i]))

    return rolls


def dmg(num_atks, mods, weapon, weapon_rolls, min_value):
    """Rolls a damage roll."""

    rolls = []
    total = 0
    for i in range(0, num_atks):
        output = []
        for j in range(0, len(weapon_rolls)):
            for _ in range(0, weapon_rolls[j]["count"]):
                roll = random.randint(1, weapon_rolls[j]["die"])
                roll = max(roll, min_value)
                output.append(roll)

        if len(output) != 0:
            rolls.append("Hit %d: %s+%d=<b>%d damage</b>" % (i + 1, "+".join([str(x) for x in output]),
                                                            mods[i], sum(output) + mods[i]))

        total += sum(output) + mods[i]

        if "dmg_static" in weapon:
            total += weapon["dmg_static"]
            rolls.append("<i>Added %s damage</i>" % weapon["dmg_static"])

    return total, rolls


def template(template, crit_attack):
    """Rolls a template."""

    rolls = []
    total = 0
    for item in template["rolls"]:
        roll_item = {
            "description": item["description"],
            "rolls": [],
            "total": 0,
            "item": item
        }
        count = item["count"]
        if crit_attack and item["crit_active"]:
            count *= item["crit_mod"]
        for _ in range(0, count):
            roll = random.randint(1, item["die"])
            roll_item["rolls"].append(roll)
            if item["mod_every"]:
                roll += item["mod"]
            roll = max(roll, item["min_value"])
            roll_item["total"] += roll
        if not item["mod_every"]:
            roll_item["total"] += item["mod"]
            roll_item["total"] = max(roll_item["total"], item["min_value"])
        rolls.append(roll_item)
        total += roll_item["total"]

    return total, rolls
