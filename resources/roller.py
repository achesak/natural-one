# -*- coding: utf-8 -*-
import random

from resources.constants import CriticalOptions
from resources.rolls import (
    BasicRollResult,
    AttackRollResult,
    TemplateRollResult,
    DamageRollDieResult,
    DamageRollStaticResult,
    DamageRollResult,
    QuickRollGroupResult,
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


def roll_damage_die(weapon, die_data, crit_attack, is_crit_roll):
    if crit_attack and 'on_critical' in die_data:
        count = die_data['on_critical']['count']
        die = die_data['on_critical']['die']
        type = die_data['on_critical']['type']
    else:
        count = die_data['count']
        die = die_data['die']
        type = die_data['type']

    roll_data = DamageRollDieResult(type)

    reroll_below = 0 if 'reroll_below' not in weapon \
        else weapon['reroll_below']

    maximize = crit_attack and 'maximize' in weapon['critical'] and weapon['critical']['maximize'] and not is_crit_roll
    multiplier = 1 if is_crit_roll or maximize or not crit_attack else weapon['critical']['multiplier']

    for _ in range(multiplier * count):
        roll = -1
        while roll <= reroll_below:
            roll = die if maximize else random.randint(1, die)
        roll_data.add_roll(roll)

    return roll_data


def roll_damage_static(weapon, static_data, crit_attack, is_crit_roll):
    if crit_attack and 'on_critical' in static_data:
        damage = static_data['on_critical']['damage']
        type = static_data['on_critical']['type']
    else:
        damage = static_data['damage']
        type = static_data['type']

    damage_data = DamageRollStaticResult(type)

    maximize = crit_attack and 'maximize' in weapon['critical'] and weapon['critical']['maximize'] and not is_crit_roll
    multiplier = 1 if is_crit_roll or maximize or not crit_attack else weapon['critical']['multiplier']

    damage_data.add_static(damage * multiplier)
    return damage_data


def roll_damage(num_atks, mods, weapon, min_value, crit_attack):
    maximize = crit_attack and 'maximize' in weapon['critical'] and weapon['critical']['maximize']
    multiplier = 1 if maximize or not crit_attack else weapon['critical']['multiplier']

    rolls = []
    total = 0
    for atk_index in range(num_atks):
        roll_result = DamageRollResult(
            atk_index + 1,
            False,
            min_value,
            mods[atk_index] * multiplier,
        )
        if 'damage_rolls' in weapon:
            for die_data in weapon['damage_rolls']:
                roll_result.add_die_roll(
                    roll_damage_die(weapon, die_data, crit_attack, False),
                )
        if 'damage_static' in weapon:
            for static_data in weapon['damage_static']:
                roll_result.add_static_damage(
                    roll_damage_static(weapon, static_data, crit_attack, False),
                )

        rolls.append(roll_result)
        total += roll_result

    if crit_attack and ('damage_rolls' in weapon['critical'] or 'damage_static' in weapon['critical']):
        for atk_index in range(num_atks):
            roll_result = DamageRollResult(
                atk_index + 1,
                True,
                min_value,
                0,
            )
            critical = weapon['critical']
            if 'damage_rolls' in critical:
                for die_data in critical['damage_rolls']:
                    roll_result.add_die_roll(
                        roll_damage_die(weapon, die_data, crit_attack, True),
                    )
            if 'damage_static' in critical:
                for static_data in critical['damage_static']:
                    roll_result.add_static_damage(
                        roll_damage_static(weapon, static_data, crit_attack, True),
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


def roll_quick(groups):
    rolls = []
    for group in groups:
        group_result = QuickRollGroupResult(group)
        group_total = 0
        for roll in group.rolls:
            if roll.is_constant:
                group_total += roll.constant
            else:
                if roll.count == 0 or roll.die == 0:
                    continue
                roll_total = 0
                for _ in range(roll.count):
                    roll_total += random.randint(1, roll.die)
                group_total += roll_total
        group_result.total = group_total
        rolls.append(group_result)
    total = sum(rolls)
    return total, rolls
