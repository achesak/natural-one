# -*- coding: utf-8 -*-
from resources.utility import sign, singularize


def format_basic(count, die, mod_each, mod_once, rolls, total):
    mod = mod_each if mod_each != 0 else mod_once
    mod_output = '{mod_sign}{mod}'.format(
        mod_sign=sign(mod),
        mod=mod
    ) if mod else ''

    output = '<span size="larger"><b>Rolled ' \
        '{count}d{die}{mod_output}: <i>{total}</i></b></span>\n'.format(
            count=count,
            die=die,
            mod_output=mod_output,
            total=total,
        )
    output += ', '.join([str(x) for x in rolls])

    return output


def format_attack(num_atks, mods, crit_range, rolls):
    output = '<span size="larger">' \
        '<b>Rolled {num_atks} attack{singular}</b>:</span>\n'.format(
            num_atks=num_atks,
            singular=singularize(num_atks),
        )
    output += '<i>Modifiers {mods}\nCritical range {crit_low}-20</i>\n'.format(
        mods=', '.join([str(x) for x in mods]),
        crit_low=crit_range,
    )
    output += '\n'.join([str(x) for x in rolls])

    return output


def format_damage(
        num_atks,
        mods,
        weapon,
        crit_attack,
        weapon_rolls,
        rolls,
        total,
):
    damage_dice = ', '.join(['{count}d{die}'.format(
        count=roll['count'],
        die=roll['die'],
    ) for roll in weapon_rolls])

    display_name = weapon['name']
    if 'display' in weapon:
        display_name = weapon['display']
    if 'no_format' not in weapon:
        display_name = display_name.lower()

    pre = ' a'
    if display_name.lower()[0] in ['a', 'e', 'i', 'o', 'u']:
        pre = ' an'
    if display_name.endswith('es'):
        pre = ''

    if crit_attack:
        weapon_hits = '{num_atks} critical hit{singular}'.format(
            num_atks=num_atks,
            singular=singularize(num_atks),
        )
    else:
        weapon_hits = '{num_atks} hit{singular}'.format(
            num_atks=num_atks,
            singular=singularize(num_atks),
        )

    output = '<span size="larger"><b>Rolled ' \
        '{hits}: <i>{total} damage</i></b></span>\n'.format(
            hits=weapon_hits,
            total=total,
        )
    output += "<i>Using{pre} {weapon}</i>".format(
        pre=pre,
        weapon=display_name,
    )
    if weapon_rolls[0]['count'] != 0:
        output += '<i>: {dice}</i>'.format(
            dice=damage_dice,
        )
    output += '\n<i>Modifiers {mods}</i>\n'.format(
        mods=', '.join([str(x) for x in mods]),
    )
    output += '\n'.join([str(x) for x in rolls])

    if crit_attack and weapon['crit_mult'] > 1:
        output += '\n<i>Multiplied by {mult}x due to critical hit</i>'.format(
            mult=weapon['crit_mult'],
        )
    elif crit_attack and 'max_on_crit' in weapon:
        output += '\n<i>Maximized due to critical hit</i>'
    elif crit_attack and weapon['crit_mult'] == 1:
        output += '\n<i>Not affected by critical it</i>'

    return output


def format_template(template, rolls, crit_attack, total):
    output = '<span size="larger">' \
        '<b>Rolled template {name}: <i>{total}</i></b></span>\n'.format(
            name=template['name'],
            total=total,
        )
    for roll in rolls:
        output += 'Rolled {desc} ({details}): <b>{roll}</b>\n'.format(
            desc=roll.item['description'],
            details=roll.roll_details,
            roll=int(roll),
        )
        output += '\t{roll}\n'.format(roll=roll)
        if crit_attack:
            output += '\t<i>{roll}</i>\n'.format(roll=roll.roll_critical)
    if output.endswith('\n'):
        output = output[:-1]

    return output


def format_initiative(name, mod, roll):
    output = '<span size="larger"><b>Rolled initiative ' \
        'for {name}: <i>{roll}</i></b></span>\n'.format(
            name=name,
            roll=roll,
        )
    output += 'Initiative: '
    if mod:
        output += '{roll}{mod}=<b>{total}</b>'.format(
            roll=roll - mod,
            mod='{sign}{mod}'.format(sign=sign(mod), mod=mod) if mod else '',
            total=roll,
        )
    else:
        output += '<b>{roll}</b>'.format(roll=roll)

    return output
