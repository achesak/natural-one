# -*- coding: utf-8 -*-


################################################################################
#
# resources/dialogs/system_dialog.py
# This dialog is used to manage systems
#
################################################################################


from gi.repository import Gtk, Gdk

import copy
import json
import os.path
import shutil
import uuid

import resources.io as io


class SystemDialog(Gtk.Dialog):

    def __init__(self, parent, systems, system_names, weapon_data):

        self.systems = copy.deepcopy(systems["systems"])
        self.system_names = copy.deepcopy(system_names)
        self.weapon_data = copy.deepcopy(weapon_data)

        Gtk.Dialog.__init__(self, "Systems", parent, Gtk.DialogFlags.MODAL, use_header_bar=True)
        self.set_size_request(500, 600)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)

        # Create the header bar.
        header = self.get_header_bar()
        header.set_title("Systems")

        # Create the main grid.
        dlg_grid = Gtk.Grid()
        dlg_grid.set_row_spacing(18)
        dlg_grid.set_column_spacing(12)
        dlg_grid.set_border_width(18)
        self.get_content_area().add(dlg_grid)

        # Create the add system grid.
        add_grid = Gtk.Grid()
        add_grid.set_row_spacing(8)
        add_grid.set_column_spacing(12)
        dlg_grid.attach(add_grid, 0, 0, 1, 1)

        # Create the add system main label.
        add_lbl = Gtk.Label()
        add_lbl.set_markup("<span size=\"x-large\">Add System</span>")
        add_lbl.set_alignment(0, 0.5)
        add_grid.attach_next_to(add_lbl, None, Gtk.PositionType.RIGHT, 2, 1)

        # Create the system file row.
        file_lbl = Gtk.Label("File")
        file_lbl.set_alignment(1, 0.5)
        add_grid.attach_next_to(file_lbl, add_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        file_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(file_btn_box.get_style_context(), "linked")
        self.file_pick_btn = Gtk.FileChooserButton("Select a file", Gtk.FileChooserAction.OPEN)
        self.file_pick_btn.set_current_folder(os.path.expanduser("~"))
        self.file_pick_btn.set_hexpand(True)
        file_btn_box.add(self.file_pick_btn)
        self.file_btn = Gtk.Button("Add")
        file_btn_box.add(self.file_btn)
        add_grid.attach_next_to(file_btn_box, file_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the systems grid.
        system_grid = Gtk.Grid()
        system_grid.set_row_spacing(5)
        system_grid.set_column_spacing(12)
        dlg_grid.attach(system_grid, 0, 2, 1, 1)

        # Create the systems main label.
        system_lbl = Gtk.Label()
        system_lbl.set_markup("<span size=\"x-large\">Manage Systems</span>")
        system_lbl.set_alignment(0, 0.5)
        system_lbl.set_margin_bottom(10)
        system_grid.attach_next_to(system_lbl, None, Gtk.PositionType.RIGHT, 1, 1)

        # Create the systems list.
        system_scroll_win = Gtk.ScrolledWindow()
        system_scroll_win.set_hexpand(True)
        system_scroll_win.set_vexpand(True)
        system_grid.attach_next_to(system_scroll_win, system_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.system_store = Gtk.ListStore(bool, str, str)
        self.system_tree = Gtk.TreeView(model=self.system_store)
        self.system_tree.set_reorderable(True)
        self.system_tree.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        enable_text = Gtk.CellRendererToggle()
        enable_text.connect("toggled", lambda widget, path: self.toggle_system_enabled(path))
        self.enable_col = Gtk.TreeViewColumn("Enabled", enable_text, active=0)
        self.system_tree.append_column(self.enable_col)
        roll_text = Gtk.CellRendererText()
        self.system_col = Gtk.TreeViewColumn("System", roll_text, text=1)
        self.system_col.set_expand(True)
        self.system_tree.append_column(self.system_col)
        source_text = Gtk.CellRendererText()
        self.source_col = Gtk.TreeViewColumn("Source", source_text, text=2)
        self.system_tree.append_column(self.source_col)
        system_scroll_win.add(self.system_tree)

        # Create the systems drag and drop help text.
        drag_sys_lbl = Gtk.Label("Drag and drop to re-arrange systems")
        drag_sys_lbl.set_margin_top(10)
        system_grid.attach_next_to(drag_sys_lbl, system_scroll_win, Gtk.PositionType.BOTTOM, 1, 1)

        self.update_systems_list()

        self.file_btn.connect("clicked", lambda x: self.add_system())
        self.system_tree.connect("drag-end", lambda x, y: self.reorder_systems())

        save_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        save_btn.set_can_default(True)
        save_btn.grab_default()

        self.show_all()

    def update_systems_list(self):
        """Updates the list of systems."""

        self.system_store.clear()
        for system in self.systems:
            source = "User" if system["user_added"] else "Base"
            self.system_store.append([system["enabled"], system["name"], source])

    def toggle_system_enabled(self, path):
        """Enable or disable systems."""

        self.system_store[path][0] = not self.system_store[path][0]
        self.systems[int(path)]["enabled"] = not self.systems[int(path)]["enabled"]

    def add_system(self):
        """Adds a new system."""

        filename = self.file_pick_btn.get_filename()
        if not filename:
            return

        errors = []
        system = None
        system_name = None

        try:
            with open(filename) as system_file:
                system = json.load(system_file)
        except (IOError, TypeError, ValueError):
            errors.append("File has significant issues. Is it in the correct format?")

        if system is not None:
            try:
                system_name = system["name"]
            except (TypeError, ValueError):
                errors.append("System name is missing.")

        if system_name in self.system_names:
            errors.append("System name is already in use.")

        if len(errors):
            error_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Add system")
            error_dialog.format_secondary_text("There was at least one issue with the selected file:\n\n" + "\n".join(errors))
            error_dialog.run()
            error_dialog.destroy()
            return

        new_filename = str(uuid.uuid4()) + ".json"
        shutil.copyfile(filename, os.path.join(io.get_systems_dir(), new_filename))

        self.systems.append({
            "name": system_name,
            "filename": new_filename,
            "enabled": True,
            "user_added": True
        })
        self.system_names.append(system_name)

        self.update_systems_list()

    def reorder_systems(self):
        """Reorders the systems list after a drag and drop."""

        new_systems = []
        for row_index in range(len(self.system_store)):
            system_name = self.system_store[row_index][1]
            original_index = -1
            for system_index in range(len(self.systems)):
                if self.systems[system_index]["name"] == system_name:
                    original_index = system_index
                    break
            new_systems.append(copy.deepcopy(self.systems[original_index]))

        self.systems = new_systems
