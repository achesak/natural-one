# -*- coding: utf-8 -*-


################################################################################
#
# resources/format.py
# This file contains functions for formatting dice roll output.
#
################################################################################


def basic(count, die, mod_each, mod_once, rolls, total):
    """Builds the output for a standard dice roll."""

    output = "<span size=\"larger\"><b>Rolled %dd%d+%d: <i>%d</i></b></span>\n" % \
             (count, die, max(mod_each, mod_once), total)
    if not mod_each:
        output += ", ".join([str(x) for x in rolls])
    else:
        output += ", ".join(["%d+%d (%d)" % (x, mod_each, x + mod_each) for x in rolls])

    return output


def atk(num_atks, mods, crit_range, rolls):
    """Builds the output for attack rolls."""

    output = "<span size=\"larger\"><b>Rolled %d attack%s</b>:</span>\n" % (num_atks, "" if num_atks == 1 else "s")
    output += "<i>Modifiers %s\nCritical range %d-20</i>\n" % (", ".join([str(x) for x in mods]), crit_range)
    output += "\n".join(rolls)

    return output


def dmg(num_atks, mods, weapon, crit_attack, weapon_rolls, rolls, total):
    """Builds the output for damage rolls."""

    damage_dice = ", ".join(["%dd%d" % (roll["count"], roll["die"]) for roll in weapon_rolls])
    display_name = weapon["name"]
    if "display" in weapon:
        display_name = weapon["display"]
    if "no_format" not in weapon:
        display_name = display_name.lower()
    use_an = display_name.lower()[0] in ["a", "e", "i", "o", "u"]
    output = "<span size=\"larger\"><b>Rolled %d hit%s with a%s %s: <i>%d damage</i></b></span>\n" % \
             (num_atks, "" if num_atks == 1 else "s", "n" if use_an else "", display_name, total)
    output += "<i>Modifiers %s\nDamage dice %s</i>\n" % (", ".join([str(x) for x in mods]), damage_dice)
    output += "\n".join(rolls) + "\n"
    if crit_attack:
        output += "<i>Multiplied by %dx due to critical hit</i>" % weapon["crit_mult"]

    return output


def template(template, rolls, crit_attack, total):
    """Builds the output for the template rolls."""

    output = "<span size=\"larger\"><b>Rolled template \"%s\": <i>%d</i></b></span>\n" % (template["name"], total)
    for roll in rolls:
        item = roll["item"]
        output += "<i>Rolled \"%s\": %d</i>\n" % (item["description"], roll["total"])
        if not item["mod_every"]:
            output += ", ".join([str(x) for x in roll["rolls"]])
        else:
            output += ", ".join(["%d+%d (%d)" % (x, item["mod"], x + item["mod"]) for x in roll["rolls"]])
        output += "\n"
    if crit_attack:
        output += "<i>Criticals applied</i>"
    if output.endswith("\n"):
        output = output[:-1]
    return output
