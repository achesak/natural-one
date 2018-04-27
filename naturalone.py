#!/usr/bin/env python
# -*- coding: utf-8 -*-


################################################################################
#
# Pathfinder Dice Roller
# Version 0.1
#
# A simple dice roller application for the Pathfinder roll playing game.
#
# Released under the GNU General Public License version 3.
#
################################################################################


# Import Gtk and Gdk for the interface.
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio
# Import necessary modules.
import sys
import random

# Import application modules.
import resources.launch as launch
import resources.format as format
import resources.roller as roller

# Import UI classes.
from resources.window import DiceRollerWindow

# Import dialogs.
from resources.dialogs.template_dialog import TemplateDialog


class DiceRoller(Gtk.Application):
    """Creates the dice roller application."""

    def __init__(self, *args, **kwargs):
        """Initializes the application."""

        super(DiceRoller, self).__init__(*args, application_id="com.achesak.diceroller", **kwargs)
        self.window = None

    def do_startup(self):
        """Application startup."""

        Gtk.Application.do_startup(self)

        # Load the application data.
        self.weapon_data = launch.get_weapon_data()["weapons"]

    def do_activate(self):
        """Application activate."""

        if not self.window:
            self.window = DiceRollerWindow(application=self, title="NaturalOne")
            self.window.set_wmclass("Pathfinder Dice Roller", "NaturalOne")

        self.setup_interface()

        self.window.present()
        self.window.show_all()

    def setup_interface(self):
        """Fills interface fields and sets events."""

        # Fill the damage roll weapon data.
        weapons = []
        for i in range(0, len(self.weapon_data)):
            weapons.append([i, self.weapon_data[i]["name"]])
        weapons.sort(key=lambda x: x[1])
        weapons.insert(0, [-1, "Choose weapon"])
        for weapon in weapons:
            self.window.weap_dam_store.append(weapon)
        self.window.weap_dam_cbox.set_active(0)

        # Fill the template list.
        for i, column_title in enumerate(["Name"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.window.template_tree.append_column(column)

        # Bind the events.
        self.window.clear_btn.connect("clicked",
                                      lambda x: self.window.results_buffer.set_text(""))
        self.window.d4_btn.connect("clicked",
                                   lambda x: self.roll(4, self.window.d4_count_ent, self.window.d4_mod_ent))
        self.window.d6_btn.connect("clicked",
                                   lambda x: self.roll(6, self.window.d6_count_ent, self.window.d6_mod_ent))
        self.window.d8_btn.connect("clicked",
                                   lambda x: self.roll(8, self.window.d8_count_ent, self.window.d8_mod_ent))
        self.window.d10_btn.connect("clicked",
                                    lambda x: self.roll(10, self.window.d10_count_ent, self.window.d10_mod_ent))
        self.window.d12_btn.connect("clicked",
                                    lambda x: self.roll(12, self.window.d12_count_ent, self.window.d12_mod_ent))
        self.window.d20_btn.connect("clicked",
                                    lambda x: self.roll(20, self.window.d20_count_ent, self.window.d20_mod_ent))
        self.window.dq_btn.connect("clicked",
                                   lambda x: self.roll_custom())
        self.window.atk_btn.connect("clicked",
                                    lambda x: self.roll_attack())
        self.window.dam_btn.connect("clicked",
                                    lambda x: self.roll_dmg())
        self.window.new_btn.connect("clicked",
                                    lambda x: self.new_template())

    def roll_custom(self):
        """Roll for custom dice."""

        # Check validity of the die.
        valid = True
        self.window.remove_error(self.window.dq_size_ent)
        try:
            die = int(self.window.dq_size_ent.get_text())
        except ValueError:
            die = 0
            self.window.add_error(self.window.dq_size_ent)
            valid = False
        
        if die < 1:
            self.window.add_error(self.window.dq_size_ent)
            valid = False

        if not valid:
            return

        self.roll(die, self.window.dq_count_ent, self.window.dq_mod_ent)

    def roll(self, die, count_ent, mod_ent):
        """Rolls the value."""

        valid = True
        self.window.remove_error(count_ent)
        self.window.remove_error(mod_ent)

        # Check validity of the entries.
        count = -1
        try:
            count = int(count_ent.get_text())
        except ValueError:
            self.window.add_error(count_ent)
            valid = False

        try:
            min_value = int(self.window.min_ent.get_text())
        except ValueError:
            self.window.add_error(self.window.min_ent)
            valid = False

        if count < 1:
            self.window.add_error(count_ent)
            valid = False

        mod = -1
        try:
            mod = int(mod_ent.get_text())
        except ValueError:
            self.window.add_error(mod_ent)
            valid = False

        if not valid:
            return

        mod_once = 0
        mod_each = mod
        if not self.window.dice_mod_chk.get_active():
            mod_once, mod_each = mod_each, mod_once

        total, rolls = roller.basic(count, die, mod_each, mod_once, min_value)
        output = format.basic(count, die, mod_each, mod_once, rolls, total)
        self.window.update_output(output)

    def roll_attack(self):
        """Rolls an attack."""
        
        valid = True
        self.window.remove_error(self.window.num_atks_ent)
        self.window.remove_error(self.window.mod_atks_ent)
        self.window.remove_error(self.window.crit_atks_ent)

        # Check validity of the entries.
        num_atks = -1
        try:
            num_atks = int(self.window.num_atks_ent.get_text())
        except ValueError:
            self.window.add_error(self.window.num_atks_ent)
            valid = False

        if num_atks < 1:
            self.window.add_error(self.window.num_atks_ent)
            valid = False

        mods = []
        try:
            mods = self.window.mod_atks_ent.get_text().split(",")
            mods = [x.strip() for x in mods]
            mods = [int(x) for x in mods]
        except ValueError:
            self.window.add_error(self.window.mod_atks_ent)
            valid = False

        if num_atks > 1 and len(mods) == 1:
            mod_value = mods[0]
            mods = [mod_value for _ in range(0, num_atks)]

        if len(mods) != num_atks:
            self.window.add_error(self.window.num_atks_ent)
            self.window.add_error(self.window.mod_atks_ent)
            valid = False

        try:
            crit_range = int(self.window.crit_atks_ent.get_text())
        except ValueError:
            self.window.add_error(self.window.crit_atks_ent)
            crit_range = -1
            valid = False
        
        if crit_range < 0 or crit_range > 20:
            self.window.add_error(self.window.crit_atks_ent)
            valid = False
        
        stop_on_crit = self.window.stop_atks_chk.get_active()

        if not valid:
            return

        rolls = roller.atk(num_atks, mods, crit_range, stop_on_crit)
        output = format.atk(num_atks, mods, crit_range, rolls)
        self.window.update_output(output)

    def roll_dmg(self):
        """Rolls damage."""

        valid = True
        self.window.remove_error(self.window.weap_dam_cbox)
        self.window.remove_error(self.window.num_dam_ent)
        self.window.remove_error(self.window.mod_dam_ent)

        # Check validity of the entries.
        weapon_index, weapon_name = -1, ""
        selected_iter = self.window.weap_dam_cbox.get_active_iter()
        if selected_iter is not None:
            weapon_index, weapon_name = self.window.weap_dam_store[selected_iter]
        if selected_iter is None or weapon_index == -1:
            self.window.add_error(self.window.weap_dam_cbox)
            valid = False

        # Check validity of the entries.
        num_atks = -1
        try:
            num_atks = int(self.window.num_dam_ent.get_text())
        except ValueError:
            self.window.add_error(self.window.num_dam_ent)
            valid = False

        if num_atks < 1:
            self.window.add_error(self.window.num_dam_ent)
            valid = False

        mods = []
        try:
            mods = self.window.mod_dam_ent.get_text().split(",")
            mods = [x.strip() for x in mods]
            mods = [int(x) for x in mods]
        except ValueError:
            self.window.add_error(self.window.mod_dam_ent)
            valid = False

        if num_atks > 1 and len(mods) == 1:
            mod_value = mods[0]
            mods = [mod_value for _ in range(0, num_atks)]

        if len(mods) != num_atks:
            self.window.add_error(self.window.num_dam_ent)
            self.window.add_error(self.window.mod_dam_ent)
            valid = False

        if self.window.small_dam_rbtn.get_active():
            die = "dmgs"
            count = "counts"
        else:
            die = "dmgm"
            count = "countm"
        crit_attack = self.window.crit_dam_chk.get_active()

        if not valid:
            return

        weapon = self.weapon_data[weapon_index]
        total, rolls = roller.dmg(num_atks, mods, weapon, count, die, crit_attack)
        output = format.dmg(num_atks, mods, weapon, crit_attack, weapon[count], weapon[die], rolls, total)
        self.window.update_output(output)

    def new_template(self):
        """Creates a new template."""

        dlg = TemplateDialog(self.window, "Create New Template")
        response = dlg.run()
        dlg.destroy()


# Show the window and start the application.
if __name__ == "__main__" and len(sys.argv) == 1:

    win = DiceRoller()
    win.run()
