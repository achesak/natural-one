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
            output += "%d%s%d=<b>%d</b>" % (self.value, mod_sign, self.mod, val)
        else:
            output += "<b>%d</b>" % self.value

        if self.status == AttackRollStatus.CRITICAL_FAIL:
            output += "\n<span color=\"red\">Critical fail!</span>"
        elif self.status == AttackRollStatus.CRITICAL or self.status == AttackRollStatus.CRITICAL_CONFIRM:
            output += "\n<span color=\"green\">Critical hit!</span>"
        if self.status == AttackRollStatus.CRITICAL_CONFIRM:
            output += " Critical confirm: "
            if self.mod:
                output += "%d+%d=<b>%d</b>" % (self.critical_value, self.mod, self.critical_value + self.mod)
            else:
                output += "<b>%d</b>" % self.critical_value

        return output


class TemplateRollResult(BasicRollResult):

    def __init__(self, item):
        super(TemplateRollResult, self).__init__()
        self.item = item
        self.rolls = []

    def add_roll(self, value):
        min_value = - float("inf") if self.item["min_value"] == "" else self.item["min_value"]
        if not self.item["mod_every"]:
            mod = 0
        else:
            mod = self.item["mod"]
        self.rolls.append(BasicRollResult(value, min_value, mod))

    @property
    def roll_details(self):
        mod_sign = "+" if self.item["mod"] > 0 else ""
        mod = "%s%d" % (mod_sign, self.item["mod"]) if self.item["mod"] else ""
        return "%dd%d%s" % (self.item["count"], self.item["die"], mod)

    @property
    def roll_critical(self):
        if self.item["crit_max"]:
            return "Maximized due to critical hit"
        elif self.item["crit_only"]:
            return "Rolled due to critical hit"
        elif self.item["crit_active"]:
            return "Multiplied by %dx due to critical hit" % self.item["crit_mod"]
        else:
            return "Not affected by critical hit"

    def __int__(self):
        min_value = - float("inf") if self.item["min_value"] == "" else self.item["min_value"]
        total = sum(self.rolls)
        if not self.item["mod_every"]:
            total += self.item["mod"]
        return max(total, min_value)

    def __str__(self):
        return ", ".join([str(x) for x in self.rolls])


class DamageRollEachResult(object):

    def __init__(self, roll_data, type):
        self.rolls = roll_data
        self.type = type

    def add_roll(self, roll):
        self.rolls.append(roll)

    def __int__(self):
        return sum(self.rolls)

    def __str__(self):
        return "+".join([str(x) for x in self.rolls])

    def __len__(self):
        return len(self.rolls)


class DamageRollResult(object):

    def __init__(self, number, crit_attack, min_value, mod):
        self.number = number
        self.crit_attack = crit_attack
        self.mod = mod
        self.min_value = min_value
        self.rolls = []
        self.dmg_static = None

    def add_weapon_roll(self, roll_data, type):
        self.rolls.append(DamageRollEachResult(roll_data, type))

    def set_static_damage(self, dmg_static, dmg_static_type):
        self.dmg_static = dmg_static
        self.dmg_static_type = dmg_static_type

    def _format_result(self):
        sorted_rolls = sorted(self.rolls, key=lambda x: x.type)
        format_list = []
        used_types = []
        index = -1
        for roll in sorted_rolls:
            if roll.type in used_types:
                format_list[index]["total"] += int(roll)
            else:
                used_types.append(roll.type)
                index += 1
                format_list.append({
                    "type": roll.type,
                    "total": int(roll)
                })
        result = []
        for format_item in format_list:
            result.append("%d %s" % (format_item["total"], format_item["type"].lower()))
        return ", ".join(result)

    def __int__(self):
        total = sum([int(x) for x in self.rolls]) + self.mod
        if self.dmg_static is not None:
            total += self.dmg_static
        return max(total, self.min_value)

    def __str__(self):
        if not self.crit_attack:
            hit_text = "Hit"
        else:
            hit_text = "Bonus critical damage"
        output = []
        if len(self.rolls) != 0 or self.dmg_static is not None:
            output.append("%s %d: <b>%s</b>" % (hit_text, self.number, self._format_result()))
        if len(self.rolls) != 0:
            for roll in self.rolls:
                if len(roll) == 1:
                    output.append("\t%d %s" % (roll, roll.type.lower()))
                else:
                    output.append("\t%s=%d %s" % (roll, roll, roll.type.lower()))
        if self.dmg_static is not None:
            output.append("\t%d %s" % (self.dmg_static, self.dmg_static_type))
        if self.mod:
            mod_sign = "+" if self.mod > 0 else ""
            output.append("\t%s%d modifier" % (mod_sign, self.mod))
        return "\n".join(output).strip()

    def __add__(self, other):
        return int(self) + other

    def __radd__(self, other):
        return other + int(self)
