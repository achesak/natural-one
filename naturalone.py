#!/usr/bin/env python
# -*- coding: utf-8 -*-


################################################################################
#
# Natural One
# Version 1.5
#
# A simple dice roller application for the Pathfinder roll playing game.
#
# Released under the GNU General Public License version 3.
#
################################################################################


import random
import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio

import resources.formatter as formatter
import resources.io as io
import resources.launch as launch
import resources.roller as roller
import resources.utility as utility

from resources.window import DiceRollerWindow

from resources.dialogs.about_dialog import NaturalOneAboutDialog
from resources.dialogs.generic_dialogs import question
from resources.dialogs.system_dialog import SystemDialog
from resources.dialogs.template_dialog import TemplateDialog


class DiceRoller(Gtk.Application):
    """Creates the dice roller application."""

    def __init__(self, *args, **kwargs):

        super(DiceRoller, self).__init__(*args, application_id="com.achesak.naturalone", **kwargs)
        self.window = None

    def do_startup(self):

        Gtk.Application.do_startup(self)

        self.templates = io.load_templates()
        self.systems = io.load_systems_settings()

        self.menu = launch.get_menu_data()
        self.style_css = launch.get_style_data()
        self.system_names, self.weapon_data = launch.get_weapon_data(self.systems)
        self.current_system_index = 0

        self.initiative_list = []

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
            self.window = DiceRollerWindow(application=self, title="Natural One", style_css=self.style_css)
            self.window.set_wmclass("Natural One", "Natural One")

        self.setup_interface()

        self.window.present()
        self.window.show_all()

    def setup_interface(self):
        """Fills interface fields and sets events."""

        self.fill_systems_list()
        self.fill_weapon_list(self.current_system_index)
        self.update_templates()

        self.window.clear_btn.connect("clicked", lambda x: self.window.results_buffer.set_text(""))
        self.window.d4_btn.connect("clicked", lambda x: self.roll(4, self.window.d4_count_ent, self.window.d4_mod_ent))
        self.window.d6_btn.connect("clicked", lambda x: self.roll(6, self.window.d6_count_ent, self.window.d6_mod_ent))
        self.window.d8_btn.connect("clicked", lambda x: self.roll(8, self.window.d8_count_ent, self.window.d8_mod_ent))
        self.window.d10_btn.connect("clicked", lambda x: self.roll(10, self.window.d10_count_ent, self.window.d10_mod_ent))
        self.window.d12_btn.connect("clicked", lambda x: self.roll(12, self.window.d12_count_ent, self.window.d12_mod_ent))
        self.window.d20_btn.connect("clicked", lambda x: self.roll(20, self.window.d20_count_ent, self.window.d20_mod_ent))
        self.window.dq_btn.connect("clicked", lambda x: self.roll_custom())
        self.window.atk_btn.connect("clicked", lambda x: self.roll_attack())
        self.window.sys_dam_cbox.connect("changed", lambda x: self.change_system())
        self.window.dam_btn.connect("clicked", lambda x: self.roll_dmg())
        self.window.weap_dam_tree.connect("row-activated", lambda x, y, z: self.roll_dmg())
        self.window.sys_manage_btn.connect("clicked", lambda x: self.manage_systems())
        self.window.new_btn.connect("clicked", lambda x: self.new_template())
        self.window.list_edit_btn.connect("clicked", lambda x: self.edit_template())
        self.window.list_delete_btn.connect("clicked", lambda x: self.remove_template())
        self.window.list_open_btn.connect("clicked", lambda x: self.import_templates())
        self.window.list_save_btn.connect("clicked", lambda x: self.export_templates())
        self.window.list_roll_btn.connect("clicked", lambda x: self.roll_template())
        self.window.template_tree.connect("row-activated", lambda x, y, z: self.roll_template())
        self.window.roll_init_rbtn.connect("toggled", lambda x: self.window.toggle_initiative_mode())
        self.window.roll_init_btn.connect("clicked", lambda x: self.roll_initiative())
        self.window.remove_init_btn.connect("clicked", lambda x: self.remove_initiative())
        self.window.clear_init_btn.connect("clicked", lambda x: self.remove_initiative(clear=True))
        self.window.init_tree.connect("drag-end", lambda x, y: self.reorder_initiative())

        self.window.register_limit_inputs()

    def fill_systems_list(self):
        """Fills the systems list."""

        self.window.sys_dam_cbox.remove_all()
        for system in self.system_names:
            self.window.sys_dam_cbox.append_text(system)
        self.window.sys_dam_cbox.set_active(0)

    def fill_weapon_list(self, index):
        """Fills the weapon list with data from the selected system."""

        self.window.weap_dam_store.clear()

        if len(self.system_names) == 0:
            return

        system_data = self.weapon_data[index]
        for i in range(0, len(system_data["data"])):
            row_iter = self.window.weap_dam_store.append(None, [system_data["data"][i]["category"]])
            for j in range(0, len(system_data["data"][i]["weapons"])):
                self.window.weap_dam_store.append(row_iter, [system_data["data"][i]["weapons"][j]["name"]])

    def change_system(self):
        """Changes the currently displayed system for weapon data."""

        current_selection = self.window.sys_dam_cbox.get_active()
        if current_selection is None or current_selection == -1:
            return

        self.current_system_index = current_selection
        self.fill_weapon_list(current_selection)

    def roll_custom(self):
        """Roll for custom dice."""

        valid = True
        self.window.remove_errors()

        # Check validity of the die.
        try:
            die = int(self.window.dq_size_ent.get_text().strip())
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

        count = self.window.int_or(count_ent, 1)
        mod = self.window.int_or(mod_ent, 0)
        mod_once, mod_each = (0, mod) if self.window.dice_mod_chk.get_active() else (mod, 0)
        min_value = self.window.int_or(self.window.min_ent, -float("inf"))

        total, rolls = roller.basic(count, die, mod_each, mod_once, min_value)
        output = formatter.basic(count, die, mod_each, mod_once, rolls, total)
        self.window.update_output(output)

    def roll_attack(self):
        """Rolls an attack."""

        self.window.remove_errors()

        num_atks = self.window.int_or(self.window.num_atks_ent, 1)
        mods = self.window.mods_or(self.window.mod_atks_ent, [0])
        mods = utility.expand_mod(mods, num_atks, False, 0)
        crit_range = self.window.int_or(self.window.crit_atks_ent, 20)

        stop_on_crit = self.window.stop_atks_chk.get_active()
        confirm_crit = self.window.confirm_atks_chk.get_active()

        rolls = roller.atk(num_atks, mods, crit_range, stop_on_crit, confirm_crit)
        output = formatter.atk(num_atks, mods, crit_range, rolls)
        self.window.update_output(output)

    def roll_dmg(self):
        """Rolls damage."""

        if len(self.system_names) == 0:
            return

        system_data = self.weapon_data[self.current_system_index]["data"]

        model, weapon_iter = self.window.weap_dam_tree.get_selection().get_selected()
        if weapon_iter is None:
            return
        section_iter = self.window.weap_dam_store.iter_parent(weapon_iter)
        if section_iter is None:
            return
        weapon = utility.get_weapon(system_data, model[weapon_iter][0], model[section_iter][0])

        crit_attack = self.window.crit_dam_chk.get_active()

        num_atks = self.window.int_or(self.window.num_dam_ent, 1)
        min_value = self.window.int_or(self.window.min_dam_ent, -float("inf"))
        mods = self.window.mods_or(self.window.mod_dam_ent, [0])

        mods = utility.expand_mod(mods, num_atks, crit_attack, weapon["crit_mult"])

        if "no_size_steps" in weapon and weapon["no_size_steps"]:
            weapon_path = "dmg"
        elif self.window.small_dam_rbtn.get_active():
            weapon_path = "dmg_small"
        else:
            weapon_path = "dmg_medium"

        total, rolls = roller.dmg(num_atks, mods, weapon, weapon_path, min_value, crit_attack)
        output = formatter.dmg(num_atks, mods, weapon, crit_attack, weapon[weapon_path], rolls, total)
        self.window.update_output(output)

    def manage_systems(self):
        """Adds or manages systems."""

        dlg = SystemDialog(self.window, self.systems, self.system_names, self.weapon_data)
        response = dlg.run()
        new_systems = dlg.systems
        dlg.destroy()

        if response != Gtk.ResponseType.OK:
            return

        self.systems["systems"] = new_systems
        self.system_names, self.weapon_data = launch.get_weapon_data(self.systems)
        io.save_systems_settings(self.systems)

        self.current_system_index = 0
        self.fill_systems_list()
        self.fill_weapon_list(self.current_system_index)

    def update_templates(self):
        """Updates the templates list."""

        self.templates.sort(key=lambda x: x["name"])

        self.window.template_store.clear()
        for template in self.templates:
            self.window.template_store.append([template["name"], len(template["rolls"])])

    def new_template(self):
        """Creates a new template."""

        dlg = TemplateDialog(self.window, "Create New Template", style_css=self.style_css)
        response = dlg.run()
        name = dlg.name_ent.get_text().strip()
        rolls = dlg.rolls
        dlg.destroy()

        if response != Gtk.ResponseType.OK or name == "" or len(rolls) == 0:
            return

        self.templates.append({
            "name": name,
            "rolls": rolls
        })

        io.save_templates(self.templates)
        self.update_templates()

    def edit_template(self):
        """Edits a template."""

        model, treeiter = self.window.template_tree.get_selection().get_selected_rows()
        index = -1
        for i in treeiter:
            index = int(str(i))

        if index == -1:
            return

        template = self.templates[index]
        dlg = TemplateDialog(self.window, template["name"], template["name"], template["rolls"], style_css=self.style_css)
        response = dlg.run()
        name = dlg.name_ent.get_text().strip()
        rolls = dlg.rolls
        dlg.destroy()

        if response != Gtk.ResponseType.OK or name == "":
            return

        if len(rolls) == 0:
            del self.templates[index]
        else:
            self.templates[index] = {
                "name": name,
                "rolls": rolls
            }

        io.save_templates(self.templates)
        self.update_templates()

    def remove_template(self):
        """Removes a template."""

        model, treeiter = self.window.template_tree.get_selection().get_selected_rows()
        indices = []
        for i in treeiter:
            indices.append(int(str(i)))

        if len(indices) == 0:
            return

        message_text = "th%s %d template%s" % ("ese" if len(indices) != 1 else "is", len(indices), "s" if len(indices) != 1 else "")
        confirm_response = question(self.window, "Templates", "Are you sure you want to remove %s?" % message_text)
        if confirm_response != Gtk.ResponseType.OK:
            return

        for index in reversed(indices):
            del self.templates[index]

        self.update_templates()

    def roll_template(self):
        """Rolls a template."""

        model, treeiter = self.window.template_tree.get_selection().get_selected_rows()
        index = -1
        for i in treeiter:
            index = int(str(i))

        if index == -1:
            return

        template = self.templates[index]
        crit_attack = self.window.list_crit_chk.get_active()

        total, rolls = roller.template(template, crit_attack)
        output = formatter.template(template, rolls, crit_attack, total)
        self.window.update_output(output)

    def import_templates(self):
        """Imports templates from a file."""

        dialog = Gtk.FileChooserDialog("Import templates", self.window, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        "Import", Gtk.ResponseType.OK))

        filter_json = Gtk.FileFilter()
        filter_json.set_name("JSON template files")
        filter_json.add_mime_type("application/json")
        dialog.add_filter(filter_json)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        response = dialog.run()
        filename = dialog.get_filename()
        dialog.destroy()

        if response != Gtk.ResponseType.OK or not filename:
            return

        new_templates = io.read_templates(filename)
        self.templates += new_templates

        io.save_templates(self.templates)
        self.update_templates()

    def export_templates(self):
        """Exports templates to a file."""

        if len(self.templates) == 0:
            return

        dialog = Gtk.FileChooserDialog("Export templates", self.window, Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        "Export", Gtk.ResponseType.OK))
        dialog.set_do_overwrite_confirmation(True)

        filter_json = Gtk.FileFilter()
        filter_json.set_name("JSON template files")
        filter_json.add_mime_type("application/json")
        dialog.add_filter(filter_json)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        response = dialog.run()
        filename = dialog.get_filename()
        dialog.destroy()

        if response != Gtk.ResponseType.OK or not filename:
            return

        io.write_templates(filename, self.templates)

    def roll_initiative(self):
        """"Rolls for an initiative."""

        self.window.remove_errors()

        name = self.window.name_init_ent.get_text().strip()
        if not name:
            self.window.add_error(self.window.name_init_ent)
            return

        mod = self.window.int_or(self.window.mod_init_ent, 0)

        if self.window.roll_init_rbtn.get_active():
            initiative, _ = roller.basic(1, 20, mod, 0, -float("inf"))
            output = formatter.initiative(name, mod, initiative)
            self.window.update_output(output)
        else:
            initiative = mod

        self.initiative_list.append({
            "name": name,
            "initiative": initiative
        })

        if self.window.sort_init_chk.get_active():
            self.initiative_list = sorted(self.initiative_list, reverse=True, key=lambda x: x["initiative"])

        self.window.init_store.clear()
        for init in self.initiative_list:
            self.window.init_store.append([init["name"], init["initiative"]])

    def remove_initiative(self, clear=False):
        """Removes initiatives from the list."""

        model, treeiter = self.window.init_tree.get_selection().get_selected_rows()
        indices = []
        for i in treeiter:
            indices.append(int(str(i)))

        if len(indices) == 0 or (clear and len(self.initiative_list) == 0):
            return

        if clear:
            message_text = "all initiatives"
        else:
            message_text = "th%s %d initiative%s" % \
                           ("ese" if len(indices) != 1 else "is", len(indices), "s" if len(indices) != 1 else "")
        confirm_response = question(self.window, "Initiatives", "Are you sure you want to remove %s?" % message_text)
        if confirm_response != Gtk.ResponseType.OK:
            return

        if not clear:
            for index in reversed(indices):
                del self.initiative_list[index]

        else:
            self.initiative_list = []

        self.window.init_store.clear()
        for init in self.initiative_list:
            self.window.init_store.append([init["name"], init["initiative"]])

    def reorder_initiative(self):
        """Reorders the initiative list after a drag and drop."""

        new_initiatives = []
        for row_index in range(len(self.window.init_store)):
            new_initiatives.append({
                "name": self.window.init_store[row_index][0],
                "initiative": self.window.init_store[row_index][1]
            })
        self.initiative_list = new_initiatives

        self.window.init_store.clear()
        for init in self.initiative_list:
            self.window.init_store.append([init["name"], init["initiative"]])

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
