# -*- coding: utf-8 -*-
import random

from resources.constants import CriticalOptions
from resources.rolls import (
    BasicRollResult,
    AttackRollResult,
    TemplateRollResult,
    DamageRollResult,
)


def roll_basic(count, die, mod_each, mod_once, min_value):
    rolls = []
    total = 0
    for _ in range(count):
        roll = random.randint(1, die)
        roll_result = BasicRollResult(roll, min_value, mod_each)
        rolls.append(roll_result)
        total += roll_result
    total += mod_once
    total = max(total, min_value)

    return total, rolls


def roll_attack(num_atks, mods, crit_range, stop_on_crit, confirm_crit):
    rolls = []
    for i in range(num_atks):
        roll = random.randint(1, 20)
        roll_result = AttackRollResult(i + 1, roll, mods[i])
        rolls.append(roll_result)
        if roll == 1 and stop_on_crit:
            break
        if roll >= crit_range and confirm_crit:
            roll_result.add_critical_confirm(random.randint(1, 20))

    return rolls


def roll_damage_die(weapon, die_data, max_damage):
    roll_data = []

    reroll_below = 0 if 'reroll_below' not in weapon \
        else weapon['reroll_below']
    for _ in range(die_data['count']):
        roll = -1
        while roll <= reroll_below:
            if max_damage:
                roll = die_data['die']
            else:
                roll = random.randint(1, die_data['die'])
        roll_data.append(roll)

    return roll_data


def roll_damage(num_atks, mods, weapon, weapon_path, min_value, crit_attack):
    weapon_rolls = weapon[weapon_path]
    apply_crit, max_damage = (False, False)
    if crit_attack and 'max_on_crit' in weapon:
        max_damage = True
    elif crit_attack:
        apply_crit = True
    crit_count = weapon['crit_mult'] if apply_crit else 1

    rolls = []
    total = 0
    for atk_index in range(num_atks):
        roll_result = DamageRollResult(
            atk_index + 1,
            False,
            min_value,
            mods[atk_index] * crit_count,
        )
        for crit_index in range(crit_count):
            for die_index in range(len(weapon_rolls)):
                die_data = weapon_rolls[die_index]
                roll_data = roll_damage_die(weapon, die_data, max_damage)
                if len(roll_data):
                    roll_result.add_weapon_roll(roll_data, die_data['type'])

        if 'dmg_static' in weapon:
            roll_result.set_static_damage(
                weapon['dmg_static'] * crit_count,
                weapon['dmg_static_type'].lower(),
            )

        rolls.append(roll_result)
        total += roll_result

    if crit_attack and 'crit_extra' in weapon:
        crit_extra = weapon['crit_extra']
        crit_rolls = crit_extra[weapon_path] \
            if weapon_path in crit_extra \
            else []
        for atk_index in range(num_atks):
            roll_result = DamageRollResult(atk_index + 1, True, min_value, 0)
            for die_index in range(len(crit_rolls)):
                die_data = crit_rolls[die_index]
                roll_data = roll_damage_die(weapon, die_data, False)
                if len(roll_data):
                    roll_result.add_weapon_roll(roll_data, die_data['type'])

            if 'dmg_static' in crit_extra:
                roll_result.set_static_damage(
                    crit_extra['dmg_static'],
                    crit_extra['dmg_static_type'].lower(),
                )

            rolls.append(roll_result)
            total += roll_result

    return total, rolls


def roll_template(template, crit_attack):
    rolls = []
    total = 0
    for item in template['rolls']:
        roll_result = TemplateRollResult(item)
        count = item['count']
        if item['crit_option'] == CriticalOptions.NONE and crit_attack:
            continue
        if item['crit_option'] == CriticalOptions.ONLY and not crit_attack:
            continue
        if item['crit_option'] == CriticalOptions.MULTIPLY and crit_attack:
            count *= item['crit_mod']
        for _ in range(count):
            if item['crit_option'] == CriticalOptions.MAXIMIZE and crit_attack:
                roll = item['die']
            else:
                roll = random.randint(1, item['die'])
            roll_result.add_roll(roll)
        rolls.append(roll_result)
        total += roll_result

    return total, rolls
