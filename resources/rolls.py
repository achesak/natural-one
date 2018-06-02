# -*- coding: utf-8 -*-


################################################################################
#
# resources/rolls.py
# This file contains classes to represent rolls.
#
################################################################################


from resources.constants import *


class BasicRollResult(object):

    def __init__(self, value, min_value, mod):
        self.value = value
        self.min_value = min_value
        self.mod = mod

    def __int__(self):
        return max(self.value + self.mod, self.min_value)

    def __str__(self):
        val = int(self)
        if self.min_value == val:
            return str(val)
        if self.mod:
            return "%d+%d (%d)" % (self.value, self.mod, val)
        return str(val)

    def __add__(self, other):
        return int(self) + other

    def __radd__(self, other):
        return other + int(self)


class AttackRollResult(BasicRollResult):

    def __init__(self, number, value, mod):
        super(AttackRollResult, self).__init__(value, 0, mod)
        self.number = number
        self.status = AttackRollStatus.NORMAL
        if value == 1:
            self.status = AttackRollStatus.CRITICAL_FAIL
        elif value == 20:
            self.status = AttackRollStatus.CRITICAL

    def add_critical_confirm(self, value):
        self.status = AttackRollStatus.CRITICAL_CONFIRM
        self.critical_value = value

    def __int__(self):
        return self.value + self.mod

    def __str__(self):
        val = int(self)
        output = "Attack %d: " % self.number
        if self.mod:
            output += "%d+%d" % (self.value, self.mod)
        else:
            output += str(self.value)
        output += "=<b>%d</b>" % val

        if self.status == AttackRollStatus.CRITICAL_FAIL:
            output += "\n<span color=\"red\">Critical fail!</span>"
        elif self.status == AttackRollStatus.CRITICAL or self.status == AttackRollStatus.CRITICAL_CONFIRM:
            output += "\n<span color=\"green\">Critical hit!</span>"
        if self.status == AttackRollStatus.CRITICAL_CONFIRM:
            output += " Critical confirm: "
            if self.mod:
                output += "%d+%d" % (self.critical_value, self.mod)
            else:
                output += str(self.critical_value)
            output += "=<b>%d</b>" % (self.critical_value + self.mod)

        return output

