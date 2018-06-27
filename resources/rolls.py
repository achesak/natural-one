# -*- coding: utf-8 -*-
from collections import defaultdict

from resources.constants import AttackRollStatus
from resources.utility import sign


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
            return '{value}{mod_sign}{mod} ({val})'.format(
                value=self.value,
                mod_sign=sign(self.mod),
                mod=self.mod,
                val=val,
            )
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
        output = 'Attack {number}: '.format(number=self.number)
        if self.mod:
            output += '{value}{mod_sign}{mod}=<b>{val}</b>'.format(
                value=self.value,
                mod_sign=sign(self.mod),
                mod=self.mod,
                val=val,
            )
        else:
            output += '<b>{value}</b>'.format(value=self.value)

        if self.status == AttackRollStatus.CRITICAL_FAIL:
            output += '\n<span color="red"><b>Critical fail!</b></span>'
        elif self.status == AttackRollStatus.CRITICAL or \
                self.status == AttackRollStatus.CRITICAL_CONFIRM:
            output += '\n<span color="green"><b>Critical hit!</b></span>'
        if self.status == AttackRollStatus.CRITICAL_CONFIRM:
            output += ' Critical confirm: '
            if self.mod:
                output += '{crit_value}{mod_sign}{mod}=<b>{val}</b>'.format(
                    crit_value=self.critical_value,
                    mod_sign=sign(self.mod),
                    mod=self.mod,
                    val=self.critical_value + self.mod,
                )
            else:
                output += '<b>{crit_value}</b>'.format(
                    crit_value=self.critical_value,
                )

        return output


class TemplateRollResult(BasicRollResult):

    def __init__(self, item):
        super(TemplateRollResult, self).__init__()
        self.item = item
        self.rolls = []

    def add_roll(self, value):
        min_value = -float('inf') \
            if self.item['min_value'] == '' \
            else self.item['min_value']
        if not self.item['mod_every']:
            mod = 0
        else:
            mod = self.item['mod']
        self.rolls.append(BasicRollResult(value, min_value, mod))

    @property
    def roll_details(self):
        mod = '{mod_sign}{mod}'.format(
            mod_sign=sign(self.item['mod']),
            mod=self.item['mod']
        ) if self.item['mod'] else ''
        return '{count}d{die}{mod}'.format(
            count=self.item['count'],
            die=self.item['die'],
            mod=mod,
        )

    @property
    def roll_critical(self):
        if self.item['crit_max']:
            return 'Maximized due to critical hit'
        elif self.item['crit_only']:
            return 'Rolled due to critical hit'
        elif self.item['crit_active']:
            return 'Multiplied by {crit_mod}x due to critical hit'.format(
                   crit_mod=self.item['crit_mod'],
            )
        else:
            return 'Not affected by critical hit'

    def __int__(self):
        min_value = -float('inf') \
            if self.item['min_value'] == '' \
            else self.item['min_value']
        total = sum(self.rolls)
        if not self.item['mod_every']:
            total += self.item['mod']
        return max(total, min_value)

    def __str__(self):
        return ', '.join([str(x) for x in self.rolls])


class DamageRollEachResult(object):

    def __init__(self, roll_data, type):
        self.rolls = roll_data
        self.type = type

    def add_roll(self, roll):
        self.rolls.append(roll)

    def __int__(self):
        return sum(self.rolls)

    def __str__(self):
        return '+'.join([str(x) for x in self.rolls])

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
        format_dict = defaultdict(int)
        for roll in self.rolls:
            format_dict[roll.type] += int(roll)
        result = []
        for type, total in format_dict.items():
            result.append('{total} {type}'.format(
                total=total,
                type=type.lower(),
            ))
        return ', '.join(result)

    def __int__(self):
        total = sum([int(x) for x in self.rolls]) + self.mod
        if self.dmg_static is not None:
            total += self.dmg_static
        return max(total, self.min_value)

    def __str__(self):
        if not self.crit_attack:
            hit_text = 'Hit'
        else:
            hit_text = 'Bonus critical damage'
        output = []
        if len(self.rolls) != 0 or self.dmg_static is not None:
            output.append('{hit_text} {number}: <b>{result}</b>'.format(
                hit_text=hit_text,
                number=self.number,
                result=self._format_result(),
            ))
        if len(self.rolls) != 0:
            for roll in self.rolls:
                if len(roll) == 1:
                    output.append('\t{roll} {type}'.format(
                        roll=roll,
                        type=roll.type.lower(),
                    ))
                else:
                    output.append('\t{roll}={roll_num} {type}'.format(
                        roll=str(roll),
                        roll_num=int(roll),
                        type=roll.type.lower(),
                    ))
        if self.dmg_static is not None:
            output.append('\t{static_amount} {static_type}'.format(
                static_amount=self.dmg_static,
                static_type=self.dmg_static_type,
            ))
        if self.mod:
            output.append('\t{mod_sign}{mod} modifier'.format(
                mod_sign=sign(self.mod),
                mod=self.mod,
            ))
        return '\n'.join(output).strip()

    def __add__(self, other):
        return int(self) + other

    def __radd__(self, other):
        return other + int(self)
