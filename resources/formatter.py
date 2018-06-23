# -*- coding: utf-8 -*-


def format_basic(count, die, mod_each, mod_once, rolls, total):
    mod = mod_each if mod_each != 0 else mod_once
    mod_sign = '+' if mod > 0 else ''
    mod_output = '%s%d' % (mod_sign, mod) if mod else ''

    output = '<span size="larger">' \
        '<b>Rolled %dd%d%s: <i>%d</i></b></span>\n' % \
        (count, die, mod_output, total)
    output += ', '.join([str(x) for x in rolls])

    return output


def format_attack(num_atks, mods, crit_range, rolls):
    output = '<span size="larger">' \
        '<b>Rolled %d attack%s</b>:</span>\n' % \
        (num_atks, '' if num_atks == 1 else 's')
    output += '<i>Modifiers %s\nCritical range %d-20</i>\n' % (
        ', '.join([str(x) for x in mods]),
        crit_range,
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
    damage_dice = ', '.join(['%dd%d' % (
        roll['count'],
        roll['die'],
    ) for roll in weapon_rolls])

    display_name = weapon['name']
    if 'display' in weapon:
        display_name = weapon['display']
    if 'no_format' not in weapon:
        display_name = display_name.lower()

    use_an = display_name.lower()[0] in ['a', 'e', 'i', 'o', 'u']

    if crit_attack:
        weapon_hits = '%d critical hit%s' % (
            num_atks,
            's' if num_atks != 1 else '',
        )
    else:
        weapon_hits = '%d hit%s' % (num_atks, 's' if num_atks != 1 else '')

    output = '<span size="larger">' \
        '<b>Rolled %s with a%s %s: <i>%d damage</i></b></span>\n' % \
        (weapon_hits, 'n' if use_an else '', display_name, total)
    output += '<i>Modifiers %s</i>\n' % ', '.join([str(x) for x in mods])

    if weapon_rolls[0]['count'] != 0:
        output += '<i>Damage dice %s</i>\n' % damage_dice
    output += '\n'.join([str(x) for x in rolls])

    if crit_attack and weapon['crit_mult'] > 1:
        output += '\n<i>Multiplied by %dx due to critical hit</i>' % \
                  weapon['crit_mult']
    elif crit_attack and 'max_on_crit' in weapon:
        output += '\n<i>Maximized due to critical hit</i>'
    elif crit_attack and weapon['crit_mult'] == 1:
        output += '\n<i>Not affected by critical it</i>'

    return output


def format_template(template, rolls, crit_attack, total):
    output = '<span size="larger">' \
        '<b>Rolled template %s: <i>%d</i></b></span>\n' % (
            template['name'],
            total,
        )
    for roll in rolls:
        output += 'Rolled %s (%s): <b>%d</b>\n' % (
            roll.item['description'],
            roll.roll_details,
            roll,
        )
        output += '\t%s\n' % roll
        if crit_attack:
            output += '\t<i>%s</i>\n' % roll.roll_critical
    if output.endswith('\n'):
        output = output[:-1]

    return output


def format_initiative(name, mod, roll):
    mod_sign = '+' if mod > 0 else ''

    output = '<span size="larger">' \
        '<b>Rolled initiative for %s: <i>%d</i></b></span>\n' % (name, roll)
    output += 'Initiative: '
    if mod:
        output += '%d%s=<b>%d</b>' % (
            roll - mod,
            '%s%d' % (mod_sign, mod) if mod else '',
            roll,
        )
    else:
        output += '<b>%d</b>' % roll

    return output
