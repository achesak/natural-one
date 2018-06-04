# -*- coding: utf-8 -*-


################################################################################
#
# resources/rolls.py
# This file contains classes to represent rolls.
#
################################################################################


from resources.constants import *


class BasicRollResult(object):

    def __init__(self, value=0, min_value=0, mod=0):
        self.value = value
        self.min_value = min_value
        self.mod = mod

    def __int__(self):
        return max(self.value + self.mod, self.min_value)

    def __str__(self):
        val = int(self)
        if self.mod:
            mod_sign = "+" if self.mod > 0 else ""
            return "%d%s%d (%d)" % (self.value, mod_sign, self.mod, val)
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
            mod_sign = "+" if self.mod > 0 else ""
            output += "%d%s%d" % (self.value, mod_sign, self.mod)
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


class TemplateRollResult(BasicRollResult):

    def __init__(self, item):
        super(TemplateRollResult, self).__init__()
        self.item = item
        self.rolls = []

    def add_roll(self, value):
        if not self.item["mod_every"]:
            mod = 0
        else:
            mod = self.item["mod"]
        self.rolls.append(BasicRollResult(value, self.item["min_value"], mod))

    def __int__(self):
        total = sum(self.rolls)
        if not self.item["mod_every"]:
            total += self.item["mod"]
        return max(total, self.item["min_value"])

    def __str__(self):
        return ", ".join([str(x) for x in self.rolls])


class DamageRollEachResult(object):

    def __init__(self, roll_data):
        self.rolls = roll_data

    def add_roll(self, roll):
        self.rolls.append(roll)

    def __int__(self):
        return sum(self.rolls)

    def __str__(self):
        return "+".join([str(x) for x in self.rolls])


class DamageRollResult(object):

    def __init__(self, number, crit_attack, min_value, mod):
        self.number = number
        self.crit_attack = crit_attack
        self.mod = mod
        self.min_value = min_value
        self.rolls = []
        self.dmg_static = None

    def add_weapon_roll(self, roll_data):
        self.rolls.append(DamageRollEachResult(roll_data))

    def set_static_damage(self, dmg_static):
        self.dmg_static = dmg_static

    def __int__(self):
        total = sum([int(x) for x in self.rolls]) + self.mod
        if self.dmg_static is not None:
            total += self.dmg_static
        return max(total, self.min_value)

    def __str__(self):
        if not self.crit_attack:
            hit_text = "Hit"
            static_text = "damage"
        else:
            hit_text = "Bonus critical damage"
            static_text = "critical damage"
        output = []
        if len(self.rolls) != 0:
            mod_sign = "+" if self.mod > 0 else ""
            output.append("%s %d: %s%s=<b>%d damage</b>" %
                          (hit_text, self.number, "+".join([str(x) for x in self.rolls]),
                           "%s%d" % (mod_sign, self.mod) if self.mod != 0 else "", int(self)))
        if self.dmg_static is not None:
            output.append("<i>Added %d %s</i>" % (self.dmg_static, static_text))
        return "\n".join(output)

    def __add__(self, other):
        return int(self) + other

    def __radd__(self, other):
        return other + int(self)
