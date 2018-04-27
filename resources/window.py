# -*- coding: utf-8 -*-


################################################################################
#
# resources/window.py
# This file defines the main UI.
#
################################################################################


# Import Gtk and Gdk for the interface.
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio


class DiceRollerWindow(Gtk.ApplicationWindow):
    """Creates the dice roller window."""

    def __init__(self, *args, **kwargs):
        super(Gtk.ApplicationWindow, self).__init__(*args, **kwargs)

        # Create the window.
        self.set_icon_from_file("resources/images/icon.png")
        self.set_size_request(900, -1)

        # Create the header bar.
        self.header = Gtk.HeaderBar()
        self.header.set_title("Dice Roller")
        self.header.set_show_close_button(True)
        self.set_titlebar(self.header)

        # Create the stack.
        self.stack = Gtk.Stack()
        self.stack.set_vexpand(False)
        self.stack.set_hexpand(False)
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.set_stack(self.stack)
        self.header.set_custom_title(self.stack_switcher)
        win_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        win_box.pack_start(self.stack, False, False, 0)
        self.add(win_box)

        # Create the header buttons.
        self.clear_btn = Gtk.Button()
        clear_img = Gtk.Image.new_from_gicon(Gio.ThemedIcon(name="edit-clear-symbolic"), Gtk.IconSize.BUTTON)
        self.clear_btn.add(clear_img)
        self.clear_btn.set_tooltip_text("Clear the output")
        self.header.pack_end(self.clear_btn)

        # Create the Basic grid.
        dice_grid = Gtk.Grid()
        dice_grid.set_row_spacing(20)
        dice_grid.set_column_spacing(20)
        dice_grid.set_border_width(20)

        # Create the dice: d4
        d4_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("resources/images/d4.png", 60, 60, True)
        d4_img = Gtk.Image.new_from_pixbuf(d4_pixbuf)
        dice_grid.attach(d4_img, 0, 0, 1, 1)
        self.d4_count_ent = Gtk.Entry()
        self.d4_count_ent.set_text("1")
        self.d4_count_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.d4_count_ent, d4_img, Gtk.PositionType.RIGHT, 1, 1)
        d4_d_lbl = Gtk.Label("d4")
        dice_grid.attach_next_to(d4_d_lbl, self.d4_count_ent, Gtk.PositionType.RIGHT, 1, 1)
        d4_plus_lbl = Gtk.Label("+")
        dice_grid.attach_next_to(d4_plus_lbl, d4_d_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.d4_mod_ent = Gtk.Entry()
        self.d4_mod_ent.set_text("0")
        self.d4_mod_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.d4_mod_ent, d4_plus_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.d4_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(self.d4_btn, self.d4_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

        # Create the dice: d6
        d6_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("resources/images/d6.png", 60, 60, True)
        d6_img = Gtk.Image.new_from_pixbuf(d6_pixbuf)
        dice_grid.attach_next_to(d6_img, d4_img, Gtk.PositionType.BOTTOM, 1, 1)
        self.d6_count_ent = Gtk.Entry()
        self.d6_count_ent.set_text("1")
        self.d6_count_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.d6_count_ent, d6_img, Gtk.PositionType.RIGHT, 1, 1)
        d6_d_lbl = Gtk.Label("d6")
        dice_grid.attach_next_to(d6_d_lbl, self.d6_count_ent, Gtk.PositionType.RIGHT, 1, 1)
        d6_plus_lbl = Gtk.Label("+")
        dice_grid.attach_next_to(d6_plus_lbl, d6_d_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.d6_mod_ent = Gtk.Entry()
        self.d6_mod_ent.set_text("0")
        self.d6_mod_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.d6_mod_ent, d6_plus_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.d6_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(self.d6_btn, self.d6_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

        # Create the dice: d8
        d8_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("resources/images/d8.png", 60, 60, True)
        d8_img = Gtk.Image.new_from_pixbuf(d8_pixbuf)
        dice_grid.attach_next_to(d8_img, d6_img, Gtk.PositionType.BOTTOM, 1, 1)
        self.d8_count_ent = Gtk.Entry()
        self.d8_count_ent.set_text("1")
        self.d8_count_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.d8_count_ent, d8_img, Gtk.PositionType.RIGHT, 1, 1)
        d8_d_lbl = Gtk.Label("d8")
        dice_grid.attach_next_to(d8_d_lbl, self.d8_count_ent, Gtk.PositionType.RIGHT, 1, 1)
        d8_plus_lbl = Gtk.Label("+")
        dice_grid.attach_next_to(d8_plus_lbl, d8_d_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.d8_mod_ent = Gtk.Entry()
        self.d8_mod_ent.set_text("0")
        self.d8_mod_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.d8_mod_ent, d8_plus_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.d8_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(self.d8_btn, self.d8_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

        # Create the dice: d10
        d10_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("resources/images/d10.png", 60, 60, True)
        d10_img = Gtk.Image.new_from_pixbuf(d10_pixbuf)
        dice_grid.attach_next_to(d10_img, d8_img, Gtk.PositionType.BOTTOM, 1, 1)
        self.d10_count_ent = Gtk.Entry()
        self.d10_count_ent.set_text("1")
        self.d10_count_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.d10_count_ent, d10_img, Gtk.PositionType.RIGHT, 1, 1)
        d10_d_lbl = Gtk.Label("d10")
        dice_grid.attach_next_to(d10_d_lbl, self.d10_count_ent, Gtk.PositionType.RIGHT, 1, 1)
        d10_plus_lbl = Gtk.Label("+")
        dice_grid.attach_next_to(d10_plus_lbl, d10_d_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.d10_mod_ent = Gtk.Entry()
        self.d10_mod_ent.set_text("0")
        self.d10_mod_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.d10_mod_ent, d10_plus_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.d10_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(self.d10_btn, self.d10_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

        # Create the dice: d12
        d12_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("resources/images/d12.png", 60, 60, True)
        d12_img = Gtk.Image.new_from_pixbuf(d12_pixbuf)
        dice_grid.attach_next_to(d12_img, d10_img, Gtk.PositionType.BOTTOM, 1, 1)
        self.d12_count_ent = Gtk.Entry()
        self.d12_count_ent.set_text("1")
        self.d12_count_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.d12_count_ent, d12_img, Gtk.PositionType.RIGHT, 1, 1)
        d12_d_lbl = Gtk.Label("d12")
        dice_grid.attach_next_to(d12_d_lbl, self.d12_count_ent, Gtk.PositionType.RIGHT, 1, 1)
        d12_plus_lbl = Gtk.Label("+")
        dice_grid.attach_next_to(d12_plus_lbl, d12_d_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.d12_mod_ent = Gtk.Entry()
        self.d12_mod_ent.set_text("0")
        self.d12_mod_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.d12_mod_ent, d12_plus_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.d12_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(self.d12_btn, self.d12_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

        # Create the dice: d20
        d20_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("resources/images/d20.png", 60, 60, True)
        d20_img = Gtk.Image.new_from_pixbuf(d20_pixbuf)
        dice_grid.attach_next_to(d20_img, d12_img, Gtk.PositionType.BOTTOM, 1, 1)
        self.d20_count_ent = Gtk.Entry()
        self.d20_count_ent.set_text("1")
        self.d20_count_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.d20_count_ent, d20_img, Gtk.PositionType.RIGHT, 1, 1)
        d20_d_lbl = Gtk.Label("d20")
        dice_grid.attach_next_to(d20_d_lbl, self.d20_count_ent, Gtk.PositionType.RIGHT, 1, 1)
        d20_plus_lbl = Gtk.Label("+")
        dice_grid.attach_next_to(d20_plus_lbl, d20_d_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.d20_mod_ent = Gtk.Entry()
        self.d20_mod_ent.set_text("0")
        self.d20_mod_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.d20_mod_ent, d20_plus_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.d20_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(self.d20_btn, self.d20_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

        # Create the dice: custom
        dq_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("resources/images/general.png", 60, 60, True)
        dq_img = Gtk.Image.new_from_pixbuf(dq_pixbuf)
        dice_grid.attach_next_to(dq_img, d20_img, Gtk.PositionType.BOTTOM, 1, 1)
        self.dq_count_ent = Gtk.Entry()
        self.dq_count_ent.set_text("1")
        self.dq_count_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.dq_count_ent, dq_img, Gtk.PositionType.RIGHT, 1, 1)
        dq_box = Gtk.Box()
        dq_d_lbl = Gtk.Label("d ")
        dq_box.add(dq_d_lbl)
        self.dq_size_ent = Gtk.Entry()
        self.dq_size_ent.set_width_chars(4)
        self.dq_size_ent.set_margin_left(5)
        dq_box.add(self.dq_size_ent)
        dice_grid.attach_next_to(dq_box, self.dq_count_ent, Gtk.PositionType.RIGHT, 1, 1)
        dq_plus_lbl = Gtk.Label("+")
        dice_grid.attach_next_to(dq_plus_lbl, dq_box, Gtk.PositionType.RIGHT, 1, 1)
        self.dq_mod_ent = Gtk.Entry()
        self.dq_mod_ent.set_text("0")
        self.dq_mod_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.dq_mod_ent, dq_plus_lbl, Gtk.PositionType.RIGHT, 1, 1)
        self.dq_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(self.dq_btn, self.dq_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

        # Create the minimum value entry.
        min_lbl = Gtk.Label("Minimum value: ")
        dice_grid.attach_next_to(min_lbl, dq_img, Gtk.PositionType.BOTTOM, 2, 1)
        self.min_ent = Gtk.Entry()
        self.min_ent.set_text("0")
        dice_grid.attach_next_to(self.min_ent, min_lbl, Gtk.PositionType.RIGHT, 4, 1);

        # Create the modifier check box.
        self.dice_mod_chk = Gtk.CheckButton("Add modifier to every roll")
        self.dice_mod_chk.set_active(True)
        self.dice_mod_chk.set_halign(Gtk.Align.CENTER)
        self.dice_mod_chk.set_hexpand(True)
        dice_grid.attach_next_to(self.dice_mod_chk, min_lbl, Gtk.PositionType.BOTTOM, 6, 1)

        # Create the Combat grid.
        combat_grid = Gtk.Grid()
        combat_grid.set_row_spacing(20)
        combat_grid.set_column_spacing(20)
        combat_grid.set_border_width(20)

        # Create the Combat -> Attack Roll grid.
        atk_grid = Gtk.Grid()
        atk_grid.set_row_spacing(5)
        atk_grid.set_column_spacing(5)
        combat_grid.attach(atk_grid, 0, 0, 1, 1)

        # Create the attack roll main label.
        atk_lbl = Gtk.Label()
        atk_lbl.set_markup("<span size=\"x-large\">Attack Roll</span>")
        atk_lbl.set_alignment(0, 0.5)
        atk_grid.add(atk_lbl)

        # Create the number of attacks row.
        num_atks_lbl = Gtk.Label("Number of attacks: ")
        num_atks_lbl.set_alignment(0, 0.5)
        atk_grid.attach_next_to(num_atks_lbl, atk_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.num_atks_ent = Gtk.Entry()
        self.num_atks_ent.set_hexpand(True)
        self.num_atks_ent.set_text("1")
        atk_grid.attach_next_to(self.num_atks_ent, num_atks_lbl, Gtk.PositionType.RIGHT, 3, 1)

        # Create the modifiers row.
        mod_atks_lbl = Gtk.Label("Modifiers: ")
        mod_atks_lbl.set_alignment(0, 0.5)
        atk_grid.attach_next_to(mod_atks_lbl, num_atks_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.mod_atks_ent = Gtk.Entry()
        self.mod_atks_ent.set_hexpand(True)
        atk_grid.attach_next_to(self.mod_atks_ent, mod_atks_lbl, Gtk.PositionType.RIGHT, 3, 1)

        # Create the critical range row.
        crit_atks_lbl = Gtk.Label("Critical range: ")
        crit_atks_lbl.set_alignment(0, 0.5)
        atk_grid.attach_next_to(crit_atks_lbl, mod_atks_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.crit_atks_ent = Gtk.Entry()
        self.crit_atks_ent.set_hexpand(True)
        self.crit_atks_ent.set_text("20")
        atk_grid.attach_next_to(self.crit_atks_ent, crit_atks_lbl, Gtk.PositionType.RIGHT, 2, 1)
        crit_20_atks_lbl = Gtk.Label("-20")
        crit_20_atks_lbl.set_alignment(0, 0.5)
        atk_grid.attach_next_to(crit_20_atks_lbl, self.crit_atks_ent, Gtk.PositionType.RIGHT, 1, 1)

        # Create the stop on fail row.
        self.stop_atks_chk = Gtk.CheckButton("Stop on critical fail")
        self.stop_atks_chk.set_active(True)
        atk_grid.attach_next_to(self.stop_atks_chk, crit_atks_lbl, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the attack roll button.
        self.atk_btn = Gtk.Button(" Roll ")
        atk_grid.attach_next_to(self.atk_btn, self.stop_atks_chk, Gtk.PositionType.RIGHT, 2, 1)

        # Create the Combat -> Damage Roll grid.
        dam_grid = Gtk.Grid()
        dam_grid.set_row_spacing(5)
        dam_grid.set_column_spacing(5)
        combat_grid.attach(dam_grid, 0, 1, 1, 1)

        # Create the damage roll main label.
        dam_lbl = Gtk.Label()
        dam_lbl.set_markup("<span size=\"x-large\">Damage Roll</span>")
        dam_lbl.set_alignment(0, 0.5)
        dam_grid.add(dam_lbl)

        # Create the weapon row.
        weap_dam_lbl = Gtk.Label("Weapon: ")
        weap_dam_lbl.set_alignment(0, 0.5)
        dam_grid.attach_next_to(weap_dam_lbl, dam_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.weap_dam_store = Gtk.ListStore(int, str)
        self.weap_dam_cbox = Gtk.ComboBox.new_with_model(self.weap_dam_store)
        self.weap_dam_cbox.set_entry_text_column(0)
        weap_dam_crend = Gtk.CellRendererText()
        self.weap_dam_cbox.pack_start(weap_dam_crend, True)
        self.weap_dam_cbox.add_attribute(weap_dam_crend, "text", 1)
        self.weap_dam_cbox.set_wrap_width(5)
        dam_grid.attach_next_to(self.weap_dam_cbox, weap_dam_lbl, Gtk.PositionType.RIGHT, 2, 1)

        # Create the number of attacks row.
        num_dam_lbl = Gtk.Label("Number of attacks: ")
        num_dam_lbl.set_alignment(0, 0.5)
        dam_grid.attach_next_to(num_dam_lbl, weap_dam_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.num_dam_ent = Gtk.Entry()
        self.num_dam_ent.set_hexpand(True)
        self.num_dam_ent.set_text("1")
        dam_grid.attach_next_to(self.num_dam_ent, num_dam_lbl, Gtk.PositionType.RIGHT, 2, 1)

        # Create the damage modifier row.
        mod_dam_lbl = Gtk.Label("Modifiers: ")
        mod_dam_lbl.set_alignment(0, 0.5)
        dam_grid.attach_next_to(mod_dam_lbl, num_dam_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.mod_dam_ent = Gtk.Entry()
        self.mod_dam_ent.set_hexpand(True)
        dam_grid.attach_next_to(self.mod_dam_ent, mod_dam_lbl, Gtk.PositionType.RIGHT, 2, 1)

        # Create the size row.
        size_dam_grid = Gtk.Grid()
        size_dam_grid.set_column_spacing(15)
        self.small_dam_rbtn = Gtk.RadioButton.new_with_label_from_widget(None, "Small")
        self.med_dam_rbtn = Gtk.RadioButton.new_with_label_from_widget(self.small_dam_rbtn, "Medium")
        self.med_dam_rbtn.set_active(True)
        size_dam_grid.add(self.small_dam_rbtn)
        size_dam_grid.attach_next_to(self.med_dam_rbtn, self.small_dam_rbtn, Gtk.PositionType.RIGHT, 1, 1)
        dam_grid.attach_next_to(size_dam_grid, mod_dam_lbl, Gtk.PositionType.BOTTOM, 4, 1)

        # Create the critical row.
        self.crit_dam_chk = Gtk.CheckButton("Critical hit")
        dam_grid.attach_next_to(self.crit_dam_chk, size_dam_grid, Gtk.PositionType.BOTTOM, 2, 1)

        # Create the damage roll button.
        self.dam_btn = Gtk.Button(" Roll ")
        dam_grid.attach_next_to(self.dam_btn, self.crit_dam_chk, Gtk.PositionType.RIGHT, 1, 1)

        # Create the Templates grid.
        templates_grid = Gtk.Grid()
        templates_grid.set_row_spacing(20)
        templates_grid.set_column_spacing(20)
        templates_grid.set_border_width(20)

        # Create the Templates -> New Template box.
        new_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        new_box.set_hexpand(True)
        templates_grid.attach(new_box, 0, 0, 1, 1)

        # Create the new template main label.
        new_lbl = Gtk.Label()
        new_lbl.set_markup("<span size=\"x-large\">New Template</span>")
        new_lbl.set_alignment(0, 0.5)
        new_box.pack_start(new_lbl, False, False, 0)

        # Create the new template button.
        self.new_btn = Gtk.Button("Create Template")
        self.new_btn.set_halign(Gtk.Align.END)
        new_box.pack_end(self.new_btn, False, False, 0)

        # Create the Templates -> Template List grid.
        list_grid = Gtk.Grid()
        list_grid.set_row_spacing(5)
        list_grid.set_column_spacing(5)
        templates_grid.attach(list_grid, 0, 1, 1, 1)

        # Create the template list main label.
        list_lbl = Gtk.Label()
        list_lbl.set_markup("<span size=\"x-large\">Templates</span>")
        list_lbl.set_alignment(0, 0.5)
        list_grid.attach_next_to(list_lbl, None, Gtk.PositionType.RIGHT, 3, 1)

        # Create the template list.
        templates_scroll_win = Gtk.ScrolledWindow()
        templates_scroll_win.set_hexpand(True)
        templates_scroll_win.set_vexpand(True)
        list_grid.attach_next_to(templates_scroll_win, list_lbl, Gtk.PositionType.BOTTOM, 3, 1)
        self.template_store = Gtk.ListStore(str)
        self.template_tree = Gtk.TreeView(model=self.template_store)
        self.template_tree.set_headers_visible(False)
        self.template_tree.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", renderer, text=0)
        self.template_tree.append_column(column)
        templates_scroll_win.add(self.template_tree)

        # Create the template list buttons.
        self.list_edit_btn = Gtk.Button("Edit")
        list_grid.attach_next_to(self.list_edit_btn, templates_scroll_win, Gtk.PositionType.BOTTOM, 1, 1)
        self.list_delete_btn = Gtk.Button("Delete")
        list_grid.attach_next_to(self.list_delete_btn, self.list_edit_btn, Gtk.PositionType.RIGHT, 1, 1)
        self.list_roll_btn = Gtk.Button("Roll")
        list_grid.attach_next_to(self.list_roll_btn, self.list_delete_btn, Gtk.PositionType.RIGHT, 1, 1)

        # Create the template list critical check box.
        self.list_crit_chk = Gtk.CheckButton("Apply critical hit")
        self.list_crit_chk.set_halign(Gtk.Align.CENTER)
        self.list_crit_chk.set_hexpand(True)
        self.list_crit_chk.set_margin_top(5)
        list_grid.attach_next_to(self.list_crit_chk, self.list_edit_btn, Gtk.PositionType.BOTTOM, 3, 1)

        # Create the results display.
        results_scroll_win = Gtk.ScrolledWindow()
        results_scroll_win.set_hexpand(True)
        results_scroll_win.set_vexpand(True)
        self.results_view = Gtk.TextView()
        self.results_view.set_editable(False)
        self.results_view.set_cursor_visible(False)
        self.results_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.results_view.set_left_margin(5)
        self.results_view.set_right_margin(5)
        self.results_view.set_top_margin(5)
        self.results_view.set_bottom_margin(5)
        self.results_buffer = self.results_view.get_buffer()
        results_scroll_win.add(self.results_view)
        win_box.pack_end(results_scroll_win, True, True, 0)

        # Create the CSS provider.
        self.style_provider = Gtk.CssProvider()
        self.style_context = Gtk.StyleContext()
        self.style_context.add_provider_for_screen(Gdk.Screen.get_default(), self.style_provider,
                                                   Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.style_provider.load_from_data(".bad-input {background-color: red}")

        # Set up the stack.
        self.stack.add_titled(dice_grid, "basic", "Basic")
        self.stack.add_titled(combat_grid, "combat", "Combat")
        self.stack.add_titled(templates_grid, "templates", "Templates")

    def add_error(self, widget):
        """Adds the error class to a widget."""

        widget.get_style_context().add_class("bad-input")

    def remove_error(self, widget):
        """Removes the error class from a widget."""

        widget.get_style_context().remove_class("bad-input")

    def update_output(self, new_text):
        """Updates the textview with new output."""

        new_text += "\n\n"
        self.results_buffer.insert_markup(self.results_buffer.get_start_iter(), new_text, len(new_text))
