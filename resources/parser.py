# -*- coding: utf-8 -*-
import re


class QuickRoll(object):

    def __init__(self, count=0, die=0, constant=0):
        self.count = count
        self.die = die
        self.constant = constant
        self.is_constant = count == 0

    def __str__(self):
        if self.is_constant:
            return str(self.constant)
        else:
            return '{count}d{die}'.format(
                count=self.count,
                die=self.die,
            )


class QuickRollGroup(object):

    def __init__(self, multiplier=1):
        self.rolls = []
        self.multiplier = multiplier

    def __str__(self):
        output = ''
        for index, roll in enumerate(self.rolls):
            output += str(roll)
            if index != len(self.rolls) - 1:
                output += '+'
        if self.multiplier != 1:
            output += 'x' + str(self.multiplier)
        return output


def is_quick_roll_valid(roll_input):
    # Ensure only valid characters are present.
    if not re.match(r'^[\d\+\*d\)\(]+$', roll_input):
        return False
    # Ensure parenthesis groupings are correct.
    last_is_open = None
    for c in roll_input:
        if c == '(':
            if last_is_open is None or not last_is_open:
                last_is_open = True
            else:
                return False
        elif c == ')':
            if last_is_open:
                last_is_open = False
            else:
                return False
    # Ensure multipliers only appear after parenthesis.
    last_location = 0
    while True:
        last_location = roll_input.find('*', last_location)
        if last_location == -1:
            break
        if last_location == 0 or roll_input[last_location - 1] != ')':
            return False
        if last_location + 1 == len(roll_input) or not roll_input[last_location + 1].isdigit():
            return False
        last_location += 1

    return True


def build_group(rolls, multiplier=1):
    group = QuickRollGroup(multiplier=multiplier)
    for roll in rolls:
        if 'd' in roll:
            loc = roll.find('d')
            group.rolls.append(QuickRoll(
                count=int(roll[0:loc]),
                die=int(roll[loc + 1:]),
            ))
        else:
            group.rolls.append(QuickRoll(constant=int(roll)))
    return group


def parse_quick_roll_input(roll_input):
    all_groups = []
    curr_group_rolls = []
    in_group = False
    pos = 0
    while pos < len(roll_input):
        if roll_input[pos].isdigit():
            end_pos = pos + 1
            if end_pos != len(roll_input):
                while roll_input[end_pos].isdigit() or roll_input[end_pos] == 'd':
                    end_pos += 1
                    if end_pos == len(roll_input):
                        break
            token = roll_input[pos:end_pos]
            pos = end_pos
            if in_group:
                curr_group_rolls.append(token)
            else:
                all_groups.append(build_group([token]))
        elif roll_input[pos] == '+':
            pos += 1
        elif roll_input[pos] == '(':
            in_group = True
            pos += 1
        elif roll_input[pos] == ')':
            in_group = False
            multiplier = 1
            if pos + 1 != len(roll_input) and roll_input[pos + 1] == '*':
                pos += 2
                end_pos = pos + 1
                if end_pos != len(roll_input):
                    while roll_input[end_pos].isdigit():
                        end_pos += 1
                        if end_pos == len(roll_input):
                            break
                multiplier = int(roll_input[pos:end_pos])
                pos = end_pos
            else:
                pos += 1
            all_groups.append(build_group(
                rolls=curr_group_rolls,
                multiplier=multiplier,
            ))
            curr_group_rolls.clear()

    return all_groups
