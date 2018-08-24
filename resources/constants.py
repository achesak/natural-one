# -*- coding: utf-8 -*-


CRITICAL_OPTIONS = [
    ['Multiply roll on critical hit', 0],
    ['Maximize roll on critical hit', 1],
    ['Roll with no change on critical hit', 2],
    ['Only roll on critical hit', 3],
    ['Do not roll on critical hit', 4],
]


class CriticalOptions(object):
    MULTIPLY = 0
    MAXIMIZE = 1
    NO_CHANGE = 2
    ONLY = 3
    NONE = 4


class AttackRollStatus(object):
    NORMAL = 0
    CRITICAL = 1
    CRITICAL_CONFIRM = 2
    CRITICAL_FAIL = 3
