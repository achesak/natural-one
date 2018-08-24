# -*- coding: utf-8 -*-
import copy

from resources.constants import SizeProgression


def get_dice_by_size(weapon, size, progression):
    adjusted_weapon = copy.deepcopy(weapon)

    diff = size - SizeProgression.MEDIUM
    if abs(diff):
        return step(adjusted_weapon, diff, progression)
    else:
        return adjusted_weapon


def get_dice_step(roll, step_by):
    if step_by > 0:
        return 1 if roll['count'] * roll['die'] <= 6 else 2
    else:
        return -1 if roll['count'] * roll['die'] <= 8 else -2


def adjust_d4(count, die):
    if count == 1:
        return count, die
    total = count * die
    if total % 8 == 0:
        return total / 8, 8
    else:
        return total / 6, 6


def adjust_d6(count, progression):
    for dice in reversed([dice for dice in progression if dice['die'] == 6]):
        if dice['count'] >= count:
            continue
        return dice['count'], 8


def adjust_d8(count, progression):
    for dice in [dice for dice in progression if dice['die'] == 8]:
        if dice['count'] <= count:
            continue
        return dice['count'], 6


def adjust_d12(count):
    return count * 2, 6


def step(weapon, step_by, progression):
    totals = [dice['count'] * dice['die'] for dice in progression]
    damage_rolls = weapon['damage_rolls']
    for roll in damage_rolls:
        dice_step = get_dice_step(roll, step_by)
        for _ in range(abs(step_by)):
            count = roll['count']
            die = roll['die']
            if die == 12:
                count, die = adjust_d12(count)
            if die == 4:
                count, die = adjust_d4(count, die)
            if count >= 2 and die == 10:
                count *=2
                die = 8
            else:
                while True:
                    total = count * die
                    if total in totals:
                        index = totals.index(total)
                        adjusted_index = max(index + dice_step, 0)
                    else:
                        if die == 6:
                            count, die = adjust_d6(count, progression)
                        elif die == 8:
                            count, die = adjust_d8(count, progression)
                        continue
                    new_roll = progression[adjusted_index]
                    count = new_roll['count']
                    die = new_roll['die']
                    break
            roll['count'] = count
            roll['die'] = die
    return weapon