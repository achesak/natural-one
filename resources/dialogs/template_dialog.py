# -*- coding: utf-8 -*-


################################################################################
#
# resources/dialogs/template_dialog.py
# This dialog is used to add and edit templates.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk, Gdk


class TemplateDialog(Gtk.Dialog):
    """Shows the template dialog."""

    def __init__(self, parent, subtitle, name=None, rolls=None):
        """Creates the dialog."""

        if rolls is None:
            rolls = []
        self.rolls = rolls
        self.name = name

        Gtk.Dialog.__init__(self, "Template", parent, Gtk.DialogFlags.MODAL, use_header_bar=True)
        self.set_size_request(600, 800)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("Save", Gtk.ResponseType.OK)

        # Create the header bar.
        header = self.get_header_bar()
        header.set_title("Template")
        header.set_subtitle(subtitle)

        # Create the main grid.
        dlg_grid = Gtk.Grid()
        dlg_grid.set_row_spacing(20)
        dlg_grid.set_column_spacing(20)
        dlg_grid.set_border_width(20)
        self.get_content_area().add(dlg_grid)

        # Create the template details grid.
        details_grid = Gtk.Grid()
        details_grid.set_row_spacing(8)
        details_grid.set_column_spacing(5)
        dlg_grid.attach(details_grid, 0, 0, 1, 1)

        # Create the template details main label.
        details_lbl = Gtk.Label()
        details_lbl.set_markup("<span size=\"x-large\">Template Details</span>")
        details_lbl.set_alignment(0, 0.5)
        details_grid.attach_next_to(details_lbl, None, Gtk.PositionType.RIGHT, 2, 1)

        # Create the template name row.
        name_lbl = Gtk.Label("Name: ")
        name_lbl.set_alignment(0, 0.5)
        details_grid.attach_next_to(name_lbl, details_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.name_ent = Gtk.Entry()
        self.name_ent.set_hexpand(True)
        details_grid.attach_next_to(self.name_ent, name_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the add roll grid.
        add_grid = Gtk.Grid()
        add_grid.set_row_spacing(8)
        add_grid.set_column_spacing(5)
        dlg_grid.attach(add_grid, 0, 1, 1, 1)

        # Create the add roll main label.
        add_lbl = Gtk.Label()
        add_lbl.set_markup("<span size=\"x-large\">Add Roll</span>")
        add_lbl.set_alignment(0, 0.5)
        add_grid.attach_next_to(add_lbl, None, Gtk.PositionType.RIGHT, 7, 1)

        # Create the roll row.
        self.count_ent = Gtk.Entry()
        self.count_ent.set_width_chars(4)
        add_grid.attach_next_to(self.count_ent, add_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        d_lbl = Gtk.Label(" d ")
        add_grid.attach_next_to(d_lbl, self.count_ent, Gtk.PositionType.RIGHT, 1, 1)
        self.die_ent = Gtk.Entry()
        self.die_ent.set_width_chars(4)
        add_grid.attach_next_to(self.die_ent, d_lbl, Gtk.PositionType.RIGHT, 1, 1)
        p_lbl = Gtk.Label(" + ")
        add_grid.attach_next_to(p_lbl, self.die_ent, Gtk.PositionType.RIGHT, 1, 1)
        self.mod_ent = Gtk.Entry()
        self.mod_ent.set_width_chars(4)
        add_grid.attach_next_to(self.mod_ent, p_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.mod_chk = Gtk.CheckButton("Add modifier to every roll")
        self.mod_chk.set_active(True)
        self.mod_chk.set_margin_left(15)
        add_grid.attach_next_to(self.mod_chk, self.mod_ent, Gtk.PositionType.RIGHT, 2, 1)

        # Create the critical rows.
        self.crit_apply_rbtn = Gtk.RadioButton.new_with_label_from_widget(None, "Multiplied by critical hit")
        self.crit_no_apply_rbtn = Gtk.RadioButton.new_with_label_from_widget(self.crit_apply_rbtn, "Not multiplied by critical hit")
        self.crit_no_apply_rbtn.set_hexpand(True)
        crit_lbl = Gtk.Label("Multiplier: ")
        crit_lbl.set_margin_left(25)
        crit_lbl.set_margin_right(5)
        self.crit_ent = Gtk.Entry()
        self.crit_ent.set_width_chars(4)
        crit_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        crit_box.pack_start(crit_lbl, False, False, 0)
        crit_box.pack_start(self.crit_ent, False, False, 0)
        add_grid.attach_next_to(self.crit_apply_rbtn, self.count_ent, Gtk.PositionType.BOTTOM, 7, 1)
        add_grid.attach_next_to(crit_box, self.crit_apply_rbtn, Gtk.PositionType.BOTTOM, 7, 1)
        add_grid.attach_next_to(self.crit_no_apply_rbtn, crit_box, Gtk.PositionType.BOTTOM, 7, 1)

        # Create the minimum value row.
        min_lbl = Gtk.Label("Minimum value: ")
        min_lbl.set_margin_right(5)
        self.min_ent = Gtk.Entry()
        self.min_ent.set_text("0")
        self.min_ent.set_hexpand(True)
        min_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        min_box.pack_start(min_lbl, False, False, 0)
        min_box.pack_start(self.min_ent, True, True, 0)
        add_grid.attach_next_to(min_box, self.crit_no_apply_rbtn, Gtk.PositionType.BOTTOM, 7, 1)

        # Create the description row.
        desc_lbl = Gtk.Label("Name: ")
        desc_lbl.set_margin_right(5)
        self.desc_ent = Gtk.Entry()
        self.desc_ent.set_hexpand(True)
        self.desc_ent.set_margin_right(5)
        self.add_btn = Gtk.Button("Add Roll")
        desc_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        desc_box.pack_start(desc_lbl, False, False, 0)
        desc_box.pack_start(self.desc_ent, True, True, 0)
        desc_box.pack_start(self.add_btn, False, False, 0)
        add_grid.attach_next_to(desc_box, min_box, Gtk.PositionType.BOTTOM, 7, 1)

        # Create the rolls grid.
        roll_grid = Gtk.Grid()
        roll_grid.set_row_spacing(8)
        roll_grid.set_column_spacing(5)
        dlg_grid.attach(roll_grid, 0, 2, 1, 1)

        # Create the rolls main label.
        roll_lbl = Gtk.Label()
        roll_lbl.set_markup("<span size=\"x-large\">Rolls</span>")
        roll_lbl.set_alignment(0, 0.5)
        roll_grid.attach_next_to(roll_lbl, None, Gtk.PositionType.RIGHT, 2, 1)

        # Create the rolls list.
        roll_scroll_win = Gtk.ScrolledWindow()
        roll_scroll_win.set_hexpand(True)
        roll_scroll_win.set_vexpand(True)
        roll_grid.attach_next_to(roll_scroll_win, roll_lbl, Gtk.PositionType.BOTTOM, 2, 1)
        self.roll_store = Gtk.ListStore(str, str, str)
        self.roll_tree = Gtk.TreeView(model=self.roll_store)
        self.roll_tree.set_headers_visible(False)
        self.roll_tree.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        desc_text = Gtk.CellRendererText()
        self.desc_col = Gtk.TreeViewColumn("Name", desc_text, text=0)
        self.desc_col.set_expand(True)
        self.roll_tree.append_column(self.desc_col)
        roll_text = Gtk.CellRendererText()
        self.roll_col = Gtk.TreeViewColumn("Roll", roll_text, text=1)
        self.roll_col.set_expand(True)
        self.roll_tree.append_column(self.roll_col)
        crit_text = Gtk.CellRendererText()
        self.crit_col = Gtk.TreeViewColumn("Critical", crit_text, text=2)
        self.crit_col.set_expand(True)
        self.roll_tree.append_column(self.crit_col)
        roll_scroll_win.add(self.roll_tree)

        # Create the rolls buttons.
        self.edit_btn = Gtk.Button("Edit")
        roll_grid.attach_next_to(self.edit_btn, roll_scroll_win, Gtk.PositionType.BOTTOM, 1, 1)
        self.delete_btn = Gtk.Button("Delete")
        roll_grid.attach_next_to(self.delete_btn, self.edit_btn, Gtk.PositionType.RIGHT, 1, 1)

        # Create the CSS provider.
        self.style_provider = Gtk.CssProvider()
        self.style_context = Gtk.StyleContext()
        self.style_context.add_provider_for_screen(Gdk.Screen.get_default(), self.style_provider,
                                                   Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.style_provider.load_from_data(".bad-input {background-color: red}")

        # Connect 'Enter' key to the Save button.
        save_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        save_btn.set_can_default(True)
        save_btn.grab_default()

        # Bind the events.
        self.add_btn.connect("clicked", lambda x: self.add_roll())
        self.edit_btn.connect("clicked", lambda x: self.edit_roll())
        self.delete_btn.connect("clicked", lambda x: self.remove_roll())
        self.roll_tree.connect("row-activated", self.activated_event)

        # Enter the default values.
        if self.name is not None:
            self.name_ent.set_text(self.name)
        self.update_list()

        # Show the dialog.
        self.show_all()

    def activated_event(self, widget, treepath, column):
        """Edits on double click."""

        tree_sel = self.roll_tree.get_selection()
        tm, ti = tree_sel.get_selected()
        self.edit_roll(ti)

    @staticmethod
    def add_error(widget):
        """Adds the error class to a widget."""

        widget.get_style_context().add_class("bad-input")

    @staticmethod
    def remove_error(widget):
        """Removes the error class from a widget."""

        widget.get_style_context().remove_class("bad-input")

    def update_list(self):
        """Updates the list."""

        self.roll_store.clear()
        for item in self.rolls:
            row = [item["description"], "%dd%d+%d" % (item["count"], item["die"], item["mod"])]
            if item["crit_active"]:
                row.append("x%d" % item["crit_mod"])
            else:
                row.append("N/A")
            self.roll_store.append(row)

    def add_roll(self):
        """Adds a roll."""

        self.remove_error(self.count_ent)
        self.remove_error(self.die_ent)
        self.remove_error(self.mod_ent)
        self.remove_error(self.crit_ent)
        self.remove_error(self.min_ent)
        self.remove_error(self.desc_ent)

        # Get the roll data.
        count = self.count_ent.get_text()
        die = self.die_ent.get_text()
        mod = self.mod_ent.get_text()
        mod_every = self.mod_chk.get_active()
        crit_mod = self.crit_ent.get_text()
        crit_active = self.crit_apply_rbtn.get_active()
        min_value = self.min_ent.get_text()
        desc = self.desc_ent.get_text().strip()

        # Check validity.
        valid = True
        try:
            count = int(count)
        except ValueError:
            self.add_error(self.count_ent)
            valid = False
        try:
            die = int(die)
        except ValueError:
            self.add_error(self.die_ent)
            valid = False
        try:
            mod = int(mod)
        except ValueError:
            self.add_error(self.mod_ent)
            valid = False
        if crit_active:
            try:
                crit_mod = int(crit_mod)
            except ValueError:
                self.add_error(self.crit_ent)
                valid = False
        try:
            min_value = int(min_value)
        except ValueError:
            self.add_error(self.min_ent)
            valid = False
        if desc == "":
            self.add_error(self.desc_ent)
            valid = False

        if not valid:
            return

        # Add the data.
        roll = {
            "description": desc,
            "count": count,
            "die": die,
            "mod": mod,
            "mod_every": mod_every,
            "crit_active": crit_active,
            "crit_mod": crit_mod,
            "min_value": min_value
        }
        add_as_new = True
        for i in range(0, len(self.rolls)):
            if self.rolls[i]["description"] == desc:
                self.rolls[i] = roll
                add_as_new = False
        if add_as_new:
            self.rolls.append(roll)

        # Update the list.
        self.update_list()

    def edit_roll(self, index=None):
        """Edits a roll."""

        # Get the selected index.
        if index is None:
            model, treeiter = self.roll_tree.get_selection().get_selected_rows()
            index = -1
            for i in treeiter:
                index = int(str(i))

        # Don't continue if nothing was selected.
        if index == -1:
            return

        # Fill the fields.
        roll = self.rolls[index]
        self.count_ent.set_text(str(roll["count"]))
        self.die_ent.set_text(str(roll["die"]))
        self.mod_ent.set_text(str(roll["mod"]))
        self.mod_chk.set_active(roll["mod_every"])
        self.crit_ent.set_text(str(roll["crit_mod"]))
        self.crit_apply_rbtn.set_active(roll["crit_active"])
        self.min_ent.set_text(str(roll["min_value"]))
        self.desc_ent.set_text(roll["description"])

    def remove_roll(self):
        """Removes a roll."""

        # Get the selected indices.
        model, treeiter = self.roll_tree.get_selection().get_selected_rows()
        indices = []
        for i in treeiter:
            indices.append(int(str(i)))

        # Don't continue if nothing was selected.
        if len(indices) == 0:
            return

        # Remove the data.
        for index in reversed(indices):
            del self.rolls[index]

        # Update the list.
        self.update_list()
