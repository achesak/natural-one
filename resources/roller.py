# -*- coding: utf-8 -*-


################################################################################
#
# resources/roller.py
# This file contains functions for generating random dice rolls.
#
################################################################################


import random
from resources.rolls import *


def basic(count, die, mod_each, mod_once, min_value):
    """Rolls dice."""

    rolls = []
    total = 0
    for _ in range(0, count):
        roll = random.randint(1, die)
        roll_result = BasicRollResult(roll, min_value, mod_each)
        rolls.append(roll_result)
        total += roll_result
    total += mod_once
    total = max(total, min_value)

    return total, rolls


def atk(num_atks, mods, crit_range, stop_on_crit, confirm_crit):
    """Rolls an attack roll."""

    rolls = []
    for i in range(0, num_atks):
        roll = random.randint(1, 20)
        roll_result = AttackRollResult(i + 1, roll, mods[i])
        rolls.append(roll_result)
        if roll == 1 and stop_on_crit:
            break
        if roll >= crit_range and confirm_crit:
            roll_result.add_critical_confirm(random.randint(1, 20))

    return rolls


def dmg(num_atks, mods, weapon, weapon_path, min_value, crit_attack):
    """Rolls a damage roll."""

    weapon_rolls = weapon[weapon_path]
    max_damage = False
    if crit_attack and "max_on_crit" in weapon:
        max_damage = True
        crit_attack = False

    rolls = []
    total = 0
    hit_num = 0
    for i in range(0, num_atks):
        if not crit_attack or (crit_attack and i % weapon["crit_mult"] == 0):
            hit_num += 1
        output = []
        for j in range(0, len(weapon_rolls)):
            for _ in range(0, weapon_rolls[j]["count"]):
                if max_damage:
                    roll = weapon_rolls[j]["die"]
                else:
                    roll = random.randint(1, weapon_rolls[j]["die"])
                if "reroll_below" in weapon:
                    while roll <= weapon["reroll_below"]:
                        if max_damage:
                            roll = weapon_rolls[j]["die"]
                        else:
                            roll = random.randint(1, weapon_rolls[j]["die"])
                roll = max(roll, min_value)
                output.append(roll)

        if len(output) != 0:
            rolls.append("Hit %d: %s+%d=<b>%d damage</b>" % (hit_num, "+".join([str(x) for x in output]), mods[i], sum(output) + mods[i]))

        total += sum(output) + mods[i]

        if "dmg_static" in weapon:
            total += weapon["dmg_static"]
            rolls.append("<i>Added %d damage</i>" % weapon["dmg_static"])

    if crit_attack and "crit_extra" in weapon:
        crit_output = []
        crit_extra = weapon["crit_extra"]
        crit_rolls = crit_extra[weapon_path] if weapon_path in crit_extra else []
        for i in range(0, num_atks / 2):
            for j in range(0, len(crit_rolls)):
                for _ in range(0, crit_rolls[j]["count"]):
                    roll = random.randint(1, crit_rolls[j]["die"])
                    crit_output.append(roll)

            if len(crit_output) != 0:
                rolls.append("Bonus critical damage %d: %s=<b>%d damage</b>" % (i + 1, "+".join([str(x) for x in crit_output]), sum(crit_output)))

            total += sum(crit_output)

            if "dmg_static" in crit_extra:
                total += crit_extra["dmg_static"]
                rolls.append("<i>Added %d critical damage</i>" % crit_extra["dmg_static"])

    return total, rolls


def template(template, crit_attack):
    """Rolls a template."""

    rolls = []
    total = 0
    for item in template["rolls"]:
        if item["crit_only"] and not crit_attack:
            continue
        roll_item = {
            "description": item["description"],
            "rolls": [],
            "total": 0,
            "item": item
        }
        count = item["count"]
        if crit_attack and item["crit_active"] and not item["crit_only"]:
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
