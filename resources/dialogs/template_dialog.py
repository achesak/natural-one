# -*- coding: utf-8 -*-
import copy

from gi.repository import Gdk, Gio, Gtk

from resources.dialogs.generic_dialogs import question
from resources.window import DiceRollerWindow


class TemplateDialog(Gtk.Dialog):

    def __init__(self, parent, subtitle, name=None, rolls=None, style_css=None):

        if rolls is None:
            rolls = []
        self.rolls = copy.deepcopy(rolls)
        self.name = name

        Gtk.Dialog.__init__(self, "Template", parent, Gtk.DialogFlags.MODAL, use_header_bar=True)
        self.set_size_request(600, 800)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)

        # Create the header bar.
        header = self.get_header_bar()
        header.set_title("Template")
        header.set_subtitle(subtitle)

        # Create the main grid.
        dlg_grid = Gtk.Grid()
        dlg_grid.set_row_spacing(18)
        dlg_grid.set_column_spacing(12)
        dlg_grid.set_border_width(18)
        self.get_content_area().add(dlg_grid)

        # Create the template details grid.
        details_grid = Gtk.Grid()
        details_grid.set_row_spacing(8)
        details_grid.set_column_spacing(12)
        dlg_grid.attach(details_grid, 0, 0, 1, 1)

        # Create the template details main label.
        details_lbl = Gtk.Label()
        details_lbl.set_markup("<span size=\"x-large\">Template Details</span>")
        details_lbl.set_alignment(0, 0.5)
        details_grid.attach_next_to(details_lbl, None, Gtk.PositionType.RIGHT, 2, 1)

        # Create the template name row.
        name_lbl = Gtk.Label("Name")
        name_lbl.set_alignment(1, 0.5)
        details_grid.attach_next_to(name_lbl, details_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.name_ent = Gtk.Entry()
        self.name_ent.set_hexpand(True)
        details_grid.attach_next_to(self.name_ent, name_lbl, Gtk.PositionType.RIGHT, 1, 1)

        # Create the add roll grid.
        add_grid = Gtk.Grid()
        add_grid.set_row_spacing(8)
        add_grid.set_column_spacing(12)
        dlg_grid.attach(add_grid, 0, 1, 1, 1)

        # Create the add roll main label.
        add_lbl = Gtk.Label()
        add_lbl.set_markup("<span size=\"x-large\">Add Roll</span>")
        add_lbl.set_alignment(0, 0.5)
        add_grid.attach_next_to(add_lbl, None, Gtk.PositionType.RIGHT, 7, 1)

        # Create the roll row.
        self.count_ent = Gtk.Entry()
        self.count_ent.set_width_chars(4)
        self.count_ent.props.xalign = 0.5
        add_grid.attach_next_to(self.count_ent, add_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        d_lbl = Gtk.Label("d")
        add_grid.attach_next_to(d_lbl, self.count_ent, Gtk.PositionType.RIGHT, 1, 1)
        self.die_ent = Gtk.Entry()
        self.die_ent.set_width_chars(4)
        self.die_ent.props.xalign = 0.5
        add_grid.attach_next_to(self.die_ent, d_lbl, Gtk.PositionType.RIGHT, 1, 1)
        p_lbl = Gtk.Label("+")
        add_grid.attach_next_to(p_lbl, self.die_ent, Gtk.PositionType.RIGHT, 1, 1)
        self.mod_ent = Gtk.Entry()
        self.mod_ent.set_width_chars(4)
        self.mod_ent.props.xalign = 0.5
        add_grid.attach_next_to(self.mod_ent, p_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.mod_chk = Gtk.CheckButton("Add modifier to every roll")
        self.mod_chk.set_active(True)
        self.mod_chk.set_margin_left(15)
        add_grid.attach_next_to(self.mod_chk, self.mod_ent, Gtk.PositionType.RIGHT, 2, 1)

        # Create the critical rows.
        self.crit_apply_rbtn = Gtk.RadioButton.new_with_label_from_widget(None, "Multiplied by critical hit")
        self.crit_apply_rbtn.set_margin_top(10)
        self.crit_max_rbtn = Gtk.RadioButton.new_with_label_from_widget(self.crit_apply_rbtn, "Maximized on critical hit")
        self.crit_no_apply_rbtn = Gtk.RadioButton.new_with_label_from_widget(self.crit_apply_rbtn, "Not multiplied by critical hit")
        self.crit_only_rbtn = Gtk.RadioButton.new_with_label_from_widget(self.crit_apply_rbtn, "Only roll on critical hit")
        self.crit_no_apply_rbtn.set_hexpand(True)
        crit_lbl = Gtk.Label("Multiplier")
        crit_lbl.set_margin_left(25)
        crit_lbl.set_margin_right(5)
        self.crit_ent = Gtk.Entry()
        self.crit_ent.set_width_chars(4)
        self.crit_ent.props.xalign = 0.5
        crit_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        crit_box.pack_start(crit_lbl, False, False, 0)
        crit_box.pack_start(self.crit_ent, False, False, 0)
        add_grid.attach_next_to(self.crit_apply_rbtn, self.count_ent, Gtk.PositionType.BOTTOM, 7, 1)
        add_grid.attach_next_to(crit_box, self.crit_apply_rbtn, Gtk.PositionType.BOTTOM, 7, 1)
        add_grid.attach_next_to(self.crit_max_rbtn, crit_box, Gtk.PositionType.BOTTOM, 7, 1)
        add_grid.attach_next_to(self.crit_no_apply_rbtn, self.crit_max_rbtn, Gtk.PositionType.BOTTOM, 7, 1)
        add_grid.attach_next_to(self.crit_only_rbtn, self.crit_no_apply_rbtn, Gtk.PositionType.BOTTOM, 7, 1)

        # Create the minimum value row.
        min_grid = Gtk.Grid()
        min_grid.set_row_spacing(5)
        min_grid.set_column_spacing(12)
        min_grid.set_margin_top(10)
        min_lbl = Gtk.Label("Minimum value")
        min_lbl.set_alignment(1, 0.5)
        self.min_ent = Gtk.Entry()
        self.min_ent.set_placeholder_text("No minimum value")
        self.min_ent.set_hexpand(True)
        min_grid.add(min_lbl)
        min_grid.attach_next_to(self.min_ent, min_lbl, Gtk.PositionType.RIGHT, 2, 1)
        add_grid.attach_next_to(min_grid, self.crit_only_rbtn, Gtk.PositionType.BOTTOM, 7, 1)

        # Create the description row.
        desc_lbl = Gtk.Label("Name")
        desc_lbl.set_alignment(1, 0.5)
        desc_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(desc_box.get_style_context(), "linked")
        self.desc_ent = Gtk.Entry()
        self.desc_ent.set_hexpand(True)
        desc_box.add(self.desc_ent)
        self.add_btn = Gtk.Button("Add Roll")
        desc_box.add(self.add_btn)
        min_grid.attach_next_to(desc_lbl, min_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        min_grid.attach_next_to(desc_box, desc_lbl, Gtk.PositionType.RIGHT, 2, 1)

        # Create the rolls grid.
        roll_grid = Gtk.Grid()
        roll_grid.set_row_spacing(0)
        roll_grid.set_column_spacing(12)
        dlg_grid.attach(roll_grid, 0, 2, 1, 1)

        # Create the rolls main label.
        roll_lbl = Gtk.Label()
        roll_lbl.set_markup("<span size=\"x-large\">Rolls</span>")
        roll_lbl.set_alignment(0, 0.5)
        roll_lbl.set_margin_bottom(10)
        roll_grid.attach_next_to(roll_lbl, None, Gtk.PositionType.RIGHT, 1, 1)

        # Create the rolls list.
        roll_scroll_win = Gtk.ScrolledWindow()
        roll_scroll_win.set_hexpand(True)
        roll_scroll_win.set_vexpand(True)
        roll_grid.attach_next_to(roll_scroll_win, roll_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.roll_store = Gtk.ListStore(str, str, str)
        self.roll_tree = Gtk.TreeView(model=self.roll_store)
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

        # Create the roll list action bar.
        self.roll_action_bar = Gtk.ActionBar()
        roll_grid.attach_next_to(self.roll_action_bar, roll_scroll_win, Gtk.PositionType.BOTTOM, 1, 1)

        # Create the template list buttons.
        roll_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(roll_btn_box.get_style_context(), "linked")
        self.roll_action_bar.pack_start(roll_btn_box)
        self.edit_btn = Gtk.Button()
        edit_img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="edit-symbolic"), Gtk.IconSize.BUTTON)
        self.edit_btn.add(edit_img)
        self.edit_btn.set_tooltip_text("Edit selected roll")
        self.delete_btn = Gtk.Button()
        delete_img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="list-remove-symbolic"), Gtk.IconSize.BUTTON)
        self.delete_btn.add(delete_img)
        self.delete_btn.set_tooltip_text("Remove selected roll")
        roll_btn_box.add(self.edit_btn)
        roll_btn_box.add(self.delete_btn)

        self.style_provider = Gtk.CssProvider()
        self.style_context = Gtk.StyleContext()
        self.style_context.add_provider_for_screen(Gdk.Screen.get_default(), self.style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.style_provider.load_from_data(style_css)

        save_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        save_btn.set_can_default(True)
        save_btn.grab_default()

        self.add_btn.connect("clicked", lambda x: self.add_roll())
        self.edit_btn.connect("clicked", lambda x: self.edit_roll())
        self.delete_btn.connect("clicked", lambda x: self.remove_roll())
        self.roll_tree.connect("row-activated", lambda x, y, z: self.edit_roll())
        self.desc_ent.connect("changed", lambda x: self.check_edit_name())

        self.register_limit_inputs()

        if self.name is not None:
            self.name_ent.set_text(self.name)
        self.update_list()

        self.show_all()

    @staticmethod
    def add_error(widget):
        """Adds the error class to a widget."""

        widget.get_style_context().add_class("bad-input")

    @staticmethod
    def remove_error(widget):
        """Removes the error class from a widget."""

        widget.get_style_context().remove_class("bad-input")

    def register_limit_inputs(self):
        """Registers which inputs should be limited."""

        number_inputs = [
            self.mod_ent, self.min_ent
        ]
        count_inputs = [
            self.count_ent, self.die_ent, self.crit_ent
        ]

        for input in number_inputs:
            input.connect("changed", DiceRollerWindow.limit_number_input)

        for input in count_inputs:
            input.connect("changed", lambda i=input: DiceRollerWindow.limit_number_input(i, allow_negative=False))

    def check_edit_name(self):
        """Checks if the current roll is being added or edited."""

        desc = self.desc_ent.get_text()
        for i in range(0, len(self.rolls)):
            if self.rolls[i]["description"] == desc:
                self.add_btn.set_label("Edit Roll")
                return

        self.add_btn.set_label("Add Roll")

    def update_list(self):
        """Updates the list."""

        self.roll_store.clear()
        for item in self.rolls:
            mod_sign = "+" if item["mod"] > 0 else ""
            mod_output = "%s%d" % (mod_sign, item["mod"]) if item["mod"] else ""
            row = [item["description"], "%dd%d%s" % (item["count"], item["die"], mod_output)]
            if item["crit_active"]:
                row.append("x%d" % item["crit_mod"])
            elif item["crit_max"]:
                row.append("Max")
            elif item["crit_only"]:
                row.append("Only")
            else:
                row.append("N/A")
            self.roll_store.append(row)

    def check_roll_validity(self, roll):
        """Ensures the user entered a valid roll."""

        self.remove_error(self.count_ent)
        self.remove_error(self.die_ent)
        self.remove_error(self.mod_ent)
        self.remove_error(self.crit_ent)
        self.remove_error(self.min_ent)
        self.remove_error(self.desc_ent)

        valid = True

        try:
            assert roll["description"] != ""
        except AssertionError:
            self.add_error(self.desc_ent)
            valid = False

        try:
            roll["count"] = int(roll["count"])
            assert roll["count"] >= 1
        except (ValueError, AssertionError):
            self.add_error(self.count_ent)
            valid = False

        try:
            roll["die"] = int(roll["die"])
            assert roll["die"] >= 1
        except (ValueError, AssertionError):
            self.add_error(self.die_ent)
            valid = False

        try:
            roll["mod"] = int(roll["mod"])
        except (ValueError, AssertionError):
            self.add_error(self.mod_ent)
            valid = False

        try:
            roll["min_value"] = int(roll["min_value"])
        except (ValueError, AssertionError):
            if roll["min_value"] != "":
                self.add_error(self.min_ent)
                valid = False

        if roll["crit_active"]:
            try:
                roll["crit_mod"] = int(roll["crit_mod"])
                assert roll["crit_mod"] >= 1
            except (ValueError, AssertionError):
                self.add_error(self.crit_ent)
                valid = False

        return valid

    def get_roll_data(self):
        """Gets the user-entered data for a roll."""

        count = self.count_ent.get_text().strip()
        die = self.die_ent.get_text().strip()
        mod = self.mod_ent.get_text().strip()
        mod_every = self.mod_chk.get_active()
        crit_mod = self.crit_ent.get_text().strip()
        crit_active = self.crit_apply_rbtn.get_active()
        crit_max = self.crit_max_rbtn.get_active()
        crit_only = self.crit_only_rbtn.get_active()
        min_value = self.min_ent.get_text().strip()
        desc = self.desc_ent.get_text().strip()

        roll = {
            "description": desc,
            "count": count,
            "die": die,
            "mod": mod,
            "mod_every": mod_every,
            "crit_active": crit_active,
            "crit_max": crit_max,
            "crit_mod": crit_mod,
            "crit_only": crit_only,
            "min_value": min_value
        }

        valid = self.check_roll_validity(roll)

        return roll, valid

    def add_roll(self):
        """Adds a roll."""

        roll, valid = self.get_roll_data()
        if not valid:
            return

        add_as_new = True
        for i in range(0, len(self.rolls)):
            if self.rolls[i]["description"] == roll["description"]:
                self.rolls[i] = roll
                add_as_new = False
        if add_as_new:
            self.rolls.append(roll)

        self.check_edit_name()

        self.update_list()

    def edit_roll(self):
        """Edits a roll."""

        model, treeiter = self.roll_tree.get_selection().get_selected_rows()
        index = -1
        for i in treeiter:
            index = int(str(i))

        if index == -1:
            return

        roll = self.rolls[index]
        self.count_ent.set_text(str(roll["count"]))
        self.die_ent.set_text(str(roll["die"]))
        self.mod_ent.set_text(str(roll["mod"]))
        self.mod_chk.set_active(roll["mod_every"])
        self.crit_ent.set_text(str(roll["crit_mod"]))
        self.crit_apply_rbtn.set_active(roll["crit_active"])
        self.crit_max_rbtn.set_active(roll["crit_max"])
        self.crit_no_apply_rbtn.set_active(not roll["crit_active"] and not roll["crit_max"] and not roll["crit_only"])
        self.crit_only_rbtn.set_active(roll["crit_only"])
        self.min_ent.set_text(str(roll["min_value"]))
        self.desc_ent.set_text(roll["description"])

        self.check_edit_name()

    def remove_roll(self):
        """Removes a roll."""

        model, treeiter = self.roll_tree.get_selection().get_selected_rows()
        indices = []
        for i in treeiter:
            indices.append(int(str(i)))

        if len(indices) == 0:
            return

        message_text = "th%s %d roll%s" % ("ese" if len(indices) != 1 else "is", len(indices), "s" if len(indices) != 1 else "")
        confirm_response = question(self, "Templates", "Are you sure you want to remove %s?" % message_text)
        if confirm_response != Gtk.ResponseType.OK:
            return

        for index in reversed(indices):
            del self.rolls[index]

        self.update_list()
