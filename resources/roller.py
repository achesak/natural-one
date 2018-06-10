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


def dmg_die(weapon, die_data, max_damage):
    """Roll damage die."""

    roll_data = []

    reroll_below = 0 if "reroll_below" not in weapon else weapon["reroll_below"]
    for _ in range(0, die_data["count"]):
        roll = -1
        while roll <= reroll_below:
            if max_damage:
                roll = die_data["die"]
            else:
                roll = random.randint(1, die_data["die"])
        roll_data.append(roll)

    return roll_data


def dmg(num_atks, mods, weapon, weapon_path, min_value, crit_attack):
    """Rolls a damage roll."""

    weapon_rolls = weapon[weapon_path]
    apply_crit, max_damage = (False, False)
    if crit_attack and "max_on_crit" in weapon:
        max_damage = True
    elif crit_attack:
        apply_crit = True
    crit_count = weapon["crit_mult"] if apply_crit else 1

    rolls = []
    total = 0
    for atk_index in range(0, num_atks):
        roll_result = DamageRollResult(atk_index + 1, False, min_value, mods[atk_index] * crit_count)
        for crit_index in range(0, crit_count):
            for die_index in range(0, len(weapon_rolls)):
                die_data = weapon_rolls[die_index]
                roll_data = dmg_die(weapon, die_data, max_damage)
                if len(roll_data):
                    roll_result.add_weapon_roll(roll_data, die_data["type"])

        if "dmg_static" in weapon:
            roll_result.set_static_damage(weapon["dmg_static"] * crit_count, weapon["dmg_static_type"].lower())

        rolls.append(roll_result)
        total += roll_result

    if crit_attack and "crit_extra" in weapon:
        crit_extra = weapon["crit_extra"]
        crit_rolls = crit_extra[weapon_path] if weapon_path in crit_extra else []
        for atk_index in range(0, num_atks):
            roll_result = DamageRollResult(atk_index + 1, True, min_value, 0)
            for die_index in range(0, len(crit_rolls)):
                die_data = crit_rolls[die_index]
                roll_data = dmg_die(weapon, die_data, False)
                if len(roll_data):
                    roll_result.add_weapon_roll(roll_data, die_data["type"])

            if "dmg_static" in crit_extra:
                roll_result.set_static_damage(crit_extra["dmg_static"], crit_extra["dmg_static_type"].lower())

            rolls.append(roll_result)
            total += roll_result

    return total, rolls


def template(template, crit_attack):
    """Rolls a template."""

    rolls = []
    total = 0
    for item in template["rolls"]:
        if item["crit_only"] and not crit_attack:
            continue
        roll_result = TemplateRollResult(item)
        count = item["count"]
        if crit_attack and item["crit_active"] and not item["crit_only"]:
            count *= item["crit_mod"]
        for _ in range(0, count):
            if crit_attack and item["crit_max"]:
                roll = item["die"]
            else:
                roll = random.randint(1, item["die"])
            roll_result.add_roll(roll)
        rolls.append(roll_result)
        total += roll_result

    return total, rolls
