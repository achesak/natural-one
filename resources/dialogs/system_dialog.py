# -*- coding: utf-8 -*-


################################################################################
#
# resources/dialogs/system_dialog.py
# This dialog is used to manage systems
#
################################################################################


from gi.repository import Gtk, Gdk

import copy


class SystemDialog(Gtk.Dialog):

    def __init__(self, parent, systems, weapon_data):

        self.systems = systems[:]
        self.weapon_data = copy.deepcopy(weapon_data)

        Gtk.Dialog.__init__(self, "Systems", parent, Gtk.DialogFlags.MODAL, use_header_bar=True)
        self.set_size_request(500, 600)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Save", Gtk.ResponseType.OK)

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
        self.system_store = Gtk.ListStore(bool, str)
        self.system_tree = Gtk.TreeView(model=self.system_store)
        self.system_tree.set_reorderable(True)
        self.system_tree.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        enable_text = Gtk.CellRendererToggle()
        enable_text.connect("toggled", self.toggle_system_enabled)
        self.enable_col = Gtk.TreeViewColumn("Enabled", enable_text, active=0)
        self.system_tree.append_column(self.enable_col)
        roll_text = Gtk.CellRendererText()
        self.system_col = Gtk.TreeViewColumn("System", roll_text, text=1)
        self.system_tree.append_column(self.system_col)
        system_scroll_win.add(self.system_tree)

        # Create the systems drag and drop help text.
        drag_sys_lbl = Gtk.Label("Drag and drop to re-arrange systems")
        drag_sys_lbl.set_margin_top(10)
        system_grid.attach_next_to(drag_sys_lbl, system_scroll_win, Gtk.PositionType.BOTTOM, 1, 1)

        # Fill the systems list.
        for i in range(len(self.systems)):
            self.system_store.append([False, self.systems[i]])

        save_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        save_btn.set_can_default(True)
        save_btn.grab_default()

        self.show_all()

    def toggle_system_enabled(self, widget, path):
        """Enable or disable systems."""

        self.system_store[path][0] = not self.system_store[path][0]

