# -*- coding: utf-8 -*-


################################################################################
#
# resources/dialogs/template_dialog.py
# This dialog is used to add and edit templates.
#
################################################################################


# Import GTK for the dialog.
from gi.repository import Gtk


class TemplateDialog(Gtk.Dialog):
    """Shows the template dialog."""

    def __init__(self, parent, subtitle):
        """Creates the dialog."""

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

        # Create the description row.
        desc_lbl = Gtk.Label("Description: ")
        desc_lbl.set_margin_right(5)
        self.desc_ent = Gtk.Entry()
        self.desc_ent.set_hexpand(True)
        self.desc_ent.set_margin_right(5)
        self.add_btn = Gtk.Button("Add Roll")
        desc_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        desc_box.pack_start(desc_lbl, False, False, 0)
        desc_box.pack_start(self.desc_ent, True, True, 0)
        desc_box.pack_start(self.add_btn, False, False, 0)
        add_grid.attach_next_to(desc_box, self.crit_no_apply_rbtn, Gtk.PositionType.BOTTOM, 7, 1)

        # Create the rolls grid.
        roll_grid = Gtk.Grid()
        roll_grid.set_row_spacing(8)
        roll_grid.set_column_spacing(5)
        dlg_grid.attach(roll_grid, 0, 2, 1, 1)

        # Create the rolls main label.
        roll_lbl = Gtk.Label()
        roll_lbl.set_markup("<span size=\"x-large\">Rolls</span>")
        roll_lbl.set_alignment(0, 0.5)
        roll_grid.attach_next_to(roll_lbl, None, Gtk.PositionType.RIGHT, 1, 1)

        # Create the rolls list.
        roll_scroll_win = Gtk.ScrolledWindow()
        roll_scroll_win.set_hexpand(True)
        roll_scroll_win.set_vexpand(True)
        roll_grid.attach_next_to(roll_scroll_win, roll_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.roll_store = Gtk.ListStore(str)
        self.roll_tree = Gtk.TreeView(model=self.roll_store)
        self.roll_tree.set_headers_visible(False)
        roll_scroll_win.add(self.roll_tree)

        # Connect 'Enter' key to the Save button.
        save_btn = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        save_btn.set_can_default(True)
        save_btn.grab_default()

        # Show the dialog.
        self.show_all()
