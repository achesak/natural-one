def basic(count, die, mod_each, mod_once, rolls, total):
    """Builds the output for a standard dice roll."""

    output = "<b>Rolled %dd%d+%d: <i>%d</i></b>\n" % (count, die, max(mod_each, mod_once), total)
    if not mod_each:
        output += ", ".join([str(x) for x in rolls])
    else:
        output += ", ".join(["%d+%d (%d)" % (x, mod_each, x + mod_each) for x in rolls])

    return output


def atk(num_atks, mods, crit_range, rolls):
    """Builds the output for attack rolls."""

    output = "<b>Rolled %d attack%s</b>:\n" % (num_atks, "" if num_atks == 1 else "s")
    output += "<i>Modifiers %s\nCritical range %d-20</i>\n" % (", ".join([str(x) for x in mods]), crit_range)
    output += "\n".join(rolls)

    return output


def dmg(num_atks, mods, weapon, crit_attack, count, die, rolls, total):
    """Builds the output for damage rolls."""

    output = "<b>Rolled %d hit%s with a %s: <i>%d damage</i></b>\n" % \
             (num_atks, "" if num_atks == 1 else "s", weapon["name"].lower(), total)
    output += "<i>Modifiers %s\nDamage dice %dd%d</i>\n" % (", ".join([str(x) for x in mods]), count, die)
    output += "\n".join(rolls) + "\n"
    if crit_attack:
        output += "<i>Multiplied by %dx due to critical hit</i>" % weapon["critm"]

    return output