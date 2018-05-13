#!/usr/bin/env python
# -*- coding: utf-8 -*-


################################################################################
#
# Natural One
# Version 1.1
#
# A simple dice roller application for the Pathfinder roll playing game.
#
# Released under the GNU General Public License version 3.
#
################################################################################


import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio

import sys
import random

import resources.launch as launch
import resources.io as io
import resources.format as format
import resources.roller as roller
import resources.utility as utility

from resources.window import DiceRollerWindow

from resources.dialogs.template_dialog import TemplateDialog
from resources.dialogs.about_dialog import NaturalOneAboutDialog


class DiceRoller(Gtk.Application):
    """Creates the dice roller application."""

    def __init__(self, *args, **kwargs):

        super(DiceRoller, self).__init__(*args, application_id="com.achesak.diceroller", **kwargs)
        self.window = None

    def do_startup(self):

        Gtk.Application.do_startup(self)

        self.menu = launch.get_menu_data()
        self.weapon_data = launch.get_weapon_data()["data"]

        self.templates = io.load_templates()

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", lambda x, y: self.about())
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", lambda x, y: self.quit())
        self.add_action(action)

        builder = Gtk.Builder.new_from_string(self.menu, -1)
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):

        if not self.window:
            self.window = DiceRollerWindow(application=self, title="Natural One")
            self.window.set_wmclass("Natural One", "Natural One")

        self.setup_interface()

        self.window.present()
        self.window.show_all()

    def setup_interface(self):
        """Fills interface fields and sets events."""

        # Fill the damage roll weapon data.
        for i in range(0, len(self.weapon_data)):
            row_iter = self.window.weap_dam_store.append(None, [self.weapon_data[i]["category"]])
            for j in range(0, len(self.weapon_data[i]["weapons"])):
                self.window.weap_dam_store.append(row_iter, [self.weapon_data[i]["weapons"][j]["name"]])

        # Fill the templates list.
        self.window.template_store.clear()
        for template in self.templates:
            self.window.template_store.append([template["name"]])

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
        self.window.dq_btn.connect("clicked", lambda x: self.roll_custom())
        self.window.atk_btn.connect("clicked", lambda x: self.roll_attack())
        self.window.dam_btn.connect("clicked", lambda x: self.roll_dmg())
        self.window.weap_dam_tree.connect("row-activated", lambda x, y, z: self.roll_dmg())
        self.window.new_btn.connect("clicked", lambda x: self.new_template())
        self.window.list_edit_btn.connect("clicked", lambda x: self.edit_template())
        self.window.list_delete_btn.connect("clicked", lambda x: self.remove_template())
        self.window.list_roll_btn.connect("clicked", lambda x: self.roll_template())
        self.window.template_tree.connect("row-activated", lambda x, y, z: self.activated_event())

    def activated_event(self):
        """Edits on double click."""

        tree_sel = self.window.template_tree.get_selection()
        tm, ti = tree_sel.get_selected()
        self.roll_template(ti)

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

        if count < 1:
            self.window.add_error(count_ent)
            valid = False

        min_value = -1
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

        mods = utility.expand_mod(mods, num_atks, False)

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
        confirm_crit = self.window.confirm_atks_chk.get_active()

        if not valid:
            return

        rolls = roller.atk(num_atks, mods, crit_range, stop_on_crit, confirm_crit)
        output = format.atk(num_atks, mods, crit_range, rolls)
        self.window.update_output(output)

    def roll_dmg(self):
        """Rolls damage."""

        valid = True
        self.window.remove_error(self.window.weap_dam_tree)
        self.window.remove_error(self.window.num_dam_ent)
        self.window.remove_error(self.window.mod_dam_ent)
        self.window.remove_error(self.window.min_dam_ent)

        # Check validity of the entries.
        model, weapon_iter = self.window.weap_dam_tree.get_selection().get_selected()
        section_iter = None
        weapon = None
        if weapon_iter is not None:
            section_iter = self.window.weap_dam_store.iter_parent(weapon_iter)
        if weapon_iter is None or section_iter is None:
            self.window.add_error(self.window.weap_dam_tree)
            valid = False
        else:
            weapon = utility.get_weapon(self.weapon_data, model[weapon_iter][0], model[section_iter][0])

        crit_attack = self.window.crit_dam_chk.get_active()

        num_atks = -1
        try:
            num_atks = int(self.window.num_dam_ent.get_text())
        except ValueError:
            self.window.add_error(self.window.num_dam_ent)
            valid = False

        if num_atks < 1:
            self.window.add_error(self.window.num_dam_ent)
            valid = False

        min_value = -1
        try:
            min_value = int(self.window.min_dam_ent.get_text())
        except ValueError:
            self.window.add_error(self.window.min_dam_ent)
            valid = False

        mods = []
        try:
            mods = self.window.mod_dam_ent.get_text().split(",")
            mods = [x.strip() for x in mods]
            mods = [int(x) for x in mods]
        except ValueError:
            self.window.add_error(self.window.mod_dam_ent)
            valid = False

        mods = utility.expand_mod(mods, num_atks, crit_attack)

        if "no_size_steps" in weapon and weapon["no_size_steps"]:
            weapon_rolls = weapon["dmg"]
        elif self.window.small_dam_rbtn.get_active():
            weapon_rolls = weapon["dmg_small"]
        else:
            weapon_rolls = weapon["dmg_medium"]

        if not valid:
            return

        if crit_attack:
            num_atks *= weapon["crit_mult"]

        total, rolls = roller.dmg(num_atks, mods, weapon, weapon_rolls, min_value)
        output = format.dmg(num_atks, mods, weapon, crit_attack, weapon_rolls, rolls, total)
        self.window.update_output(output)

    def new_template(self):
        """Creates a new template."""

        dlg = TemplateDialog(self.window, "Create New Template")
        response = dlg.run()
        name = dlg.name_ent.get_text().strip()
        rolls = dlg.rolls
        dlg.destroy()

        if response != Gtk.ResponseType.OK or name == "" or len(rolls) == 0:
            return

        template = {
            "name": name,
            "rolls": rolls
        }
        self.templates.append(template)

        io.save_templates(self.templates)

        self.window.template_store.clear()
        for template in self.templates:
            self.window.template_store.append([template["name"]])

    def edit_template(self):
        """Edits a template."""

        model, treeiter = self.window.template_tree.get_selection().get_selected_rows()
        index = -1
        for i in treeiter:
            index = int(str(i))

        if index == -1:
            return

        template = self.templates[index]
        dlg = TemplateDialog(self.window, template["name"], template["name"], template["rolls"])
        response = dlg.run()
        name = dlg.name_ent.get_text().strip()
        rolls = dlg.rolls
        dlg.destroy()

        if response != Gtk.ResponseType.OK or name == "" or len(rolls) == 0:
            return

        new_template = {
            "name": name,
            "rolls": rolls
        }
        self.templates[index] = new_template

        io.save_templates(self.templates)

        self.window.template_store.clear()
        for template in self.templates:
            self.window.template_store.append([template["name"]])

    def remove_template(self):
        """Removes a template."""

        model, treeiter = self.window.template_tree.get_selection().get_selected_rows()
        indices = []
        for i in treeiter:
            indices.append(int(str(i)))

        if len(indices) == 0:
            return

        for index in reversed(indices):
            del self.templates[index]

        self.window.template_store.clear()
        for template in self.templates:
            self.window.template_store.append([template["name"]])

    def roll_template(self, index=None):
        """Rolls a template."""

        if index is None:
            model, treeiter = self.window.template_tree.get_selection().get_selected_rows()
            index = -1
            for i in treeiter:
                index = int(str(i))

        if index == -1:
            return

        template = self.templates[index]
        crit_attack = self.window.list_crit_chk.get_active()

        total, rolls = roller.template(template, crit_attack)
        output = format.template(template, rolls, crit_attack, total)
        self.window.update_output(output)

    def about(self):
        """Shows the About dialog."""

        with open("resources/images/icon256.png", "rb") as img_file:
            img_bin = img_file.read()

        loader = GdkPixbuf.PixbufLoader.new_with_type("png")
        loader.write(img_bin)
        loader.close()
        pixbuf = loader.get_pixbuf()

        about_dlg = NaturalOneAboutDialog(self.window, pixbuf)
        about_dlg.run()
        about_dlg.destroy()


if __name__ == "__main__":

    win = DiceRoller()
    win.run()
