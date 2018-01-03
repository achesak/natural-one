import random


def basic(count, die, mod_each, mod_once):
    """Rolls dice."""

    rolls = []
    total = 0
    for _ in range(0, count):
        roll = random.randint(1, die)
        total += roll
        if mod_each:
            total += mod_each
        rolls.append(roll)
    total += mod_once

    return total, rolls


def atk(num_atks, mods, crit_range, stop_on_crit):
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
            confirm = random.randint(1, 20)
            rolls.append("Critical confirm: %d+%d=<b>%d</b>" % (confirm, mods[i], confirm + mods[i]))

    return rolls


def dmg(num_atks, mods, weapon, count, die, crit_attack):
    """Rolls a damage roll."""

    rolls = []
    total = 0
    for i in range(0, num_atks):
        output = []
        for _ in range(0, weapon[count]):
            roll = random.randint(1, weapon[die])
            output.append(roll)
        rolls.append("Hit %d: %s+%d=<b>%d damage</b>" % (i + 1, "+".join([str(x) for x in output]),
                                                         mods[i], sum(output) + mods[i]))
        total += sum(output) + mods[i]

    if crit_attack:
        total *= weapon["critm"]

    return total, rolls