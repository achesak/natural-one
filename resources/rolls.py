import random


def roll(count, die, mod_each, mod_once):
    """Rolls dice."""

    rolls = []
    total = 0
    for _ in range(0, count):
        roll = random.randint(1, die)
        total += roll
        output = str(roll)
        if add_each:
            total += add_each
            output += "+%d (%d)" % (add_each, roll + add_each)
        rolls.append(output)
    total += add_once


def atk():
    """Rolls an attack roll."""


def dmg():
    """Rolls a damage roll."""