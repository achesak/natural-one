# Import Gtk and Gdk for the interface.
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio
# Import necessary modules.
import sys
import random

import resources.launch as launch


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
            self.window = Gtk.ApplicationWindow(application=self, title="Dice Roller")
            self.window.set_wmclass("Dice Roller", "Dice Roller")

        self.create_interface()

        self.window.present()
        self.window.show_all()

    def create_interface(self):
        """Creates the user interface."""

        # Create the window.
        self.window.set_icon_from_file("resources/images/icon.png")
        self.window.set_size_request(900, -1)

        # Create the header bar.
        self.header = Gtk.HeaderBar()
        self.header.set_title("Dice Roller")
        self.header.set_show_close_button(True)
        self.window.set_titlebar(self.header)

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
        self.window.add(win_box)

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
        d4_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(d4_btn, self.d4_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

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
        d6_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(d6_btn, self.d6_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

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
        d8_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(d8_btn, self.d8_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

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
        d10_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(d10_btn, self.d10_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

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
        d12_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(d12_btn, self.d12_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

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
        d20_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(d20_btn, self.d20_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

        # Create the dice: custom
        dq_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("resources/images/general.png", 60, 60, True)
        dq_img = Gtk.Image.new_from_pixbuf(dq_pixbuf)
        dice_grid.attach_next_to(dq_img, d20_img, Gtk.PositionType.BOTTOM, 1, 1)
        self.dq_count_ent = Gtk.Entry()
        self.dq_count_ent.set_text("1")
        self.dq_count_ent.set_width_chars(4)
        dice_grid.attach_next_to(self.dq_count_ent, dq_img, Gtk.PositionType.RIGHT, 1, 1)
        dq_box = Gtk.Box()
        dq_d_lbl = Gtk.Label("d")
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
        dq_btn = Gtk.Button(" Roll ")
        dice_grid.attach_next_to(dq_btn, self.dq_mod_ent, Gtk.PositionType.RIGHT, 1, 1)

        # Create the modifier check box.
        self.dice_mod_chk = Gtk.CheckButton("Add modifier to every roll")
        self.dice_mod_chk.set_active(True)
        self.dice_mod_chk.set_halign(Gtk.Align.CENTER)
        self.dice_mod_chk.set_hexpand(True)
        dice_grid.attach_next_to(self.dice_mod_chk, dq_img, Gtk.PositionType.BOTTOM, 6, 1)

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
        weapons = []
        for i in range(0, len(self.weapon_data)):
            weapons.append([i, self.weapon_data[i]["name"]])
        weapons.sort(key=lambda x: x[1])
        weapons.insert(0, [-1, "Choose weapon"])
        for weapon in weapons:
            self.weap_dam_store.append(weapon)
        self.weap_dam_cbox = Gtk.ComboBox.new_with_model(self.weap_dam_store)
        self.weap_dam_cbox.set_active(0)
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
        for i, column_title in enumerate(["Name"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
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

        # Bind the events.
        self.clear_btn.connect("clicked", lambda x: self.results_buffer.set_text(""))
        d4_btn.connect("clicked", lambda x: self.roll(4, self.d4_count_ent, self.d4_mod_ent))
        d6_btn.connect("clicked", lambda x: self.roll(6, self.d6_count_ent, self.d6_mod_ent))
        d8_btn.connect("clicked", lambda x: self.roll(8, self.d8_count_ent, self.d8_mod_ent))
        d10_btn.connect("clicked", lambda x: self.roll(10, self.d10_count_ent, self.d10_mod_ent))
        d12_btn.connect("clicked", lambda x: self.roll(12, self.d12_count_ent, self.d12_mod_ent))
        d20_btn.connect("clicked", lambda x: self.roll(20, self.d20_count_ent, self.d20_mod_ent))
        dq_btn.connect("clicked", lambda x: self.roll_custom())
        self.atk_btn.connect("clicked", lambda x: self.roll_attack())
        self.dam_btn.connect("clicked", lambda x: self.roll_dmg())

    def update_output(self, new_text):
        """Updates the textview with new output."""

        self.results_buffer.insert_markup(self.results_buffer.get_start_iter(), new_text, len(new_text))
    
    def build_output(self, die, count, mod, rolls, total):
        """Builds the roll output."""

        output = "<b>Rolled %dd%d + %d: <i>%d</i></b>\n" % (count, die, mod, total)
        output += ", ".join(rolls) + "\n\n"
        self.update_output(output)

    def build_attack_output(self, num_atks, mods, crit_range, rolls):
        """Builds the attack roll output."""

        output = "<b>Rolled %d attack%s</b>:\n" % (num_atks, "" if num_atks == 1 else "s")
        output += "<i>Modifiers %s\nCritical range %d-20</i>\n" % (", ".join([str(x) for x in mods]), crit_range)
        output += "\n".join(rolls) + "\n\n"
        self.update_output(output)

    def build_dmg_output(self, num_atks, mods, weapon_name, rolls, total, crit_attack, critm, size, count):
        """Builds the damage roll output."""

        output = "<b>Rolled %d hit%s with a %s: <i>%d damage</i></b>\n" %\
                 (num_atks, "" if num_atks == 1 else "s", weapon_name.lower(), total)
        output += "<i>Modifiers %s\nDamage dice %dd%d</i>\n" % (", ".join([str(x) for x in mods]), count, size)
        output += "\n".join(rolls) + "\n"
        if crit_attack:
            output += "<i>Multiplied by a %dx critical multiplier</i>" % critm
        output += "\n\n"
        self.update_output(output)

    def roll_custom(self):
        """Roll for custom dice."""

        # Check validity of the die.
        self.dq_size_ent.get_style_context().remove_class("bad-input")
        try:
            die = int(self.dq_size_ent.get_text())
        except ValueError:
            self.dq_size_ent.get_style_context().add_class("bad-input")
            return

        if die < 1:
            self.dq_size_ent.get_style_context().add_class("bad-input")
            return

        self.roll(die, self.dq_count_ent, self.dq_mod_ent)

    def roll(self, die, count_ent, mod_ent):
        """Rolls the value."""

        count_ent.get_style_context().remove_class("bad-input")
        mod_ent.get_style_context().remove_class("bad-input")

        # Check validity of the entries.
        try:
            count = int(count_ent.get_text())
        except ValueError:
            count_ent.get_style_context().add_class("bad-input")
            return

        if count < 1:
            count_ent.get_style_context().add_class("bad-input")

        try:
            mod = int(mod_ent.get_text())
        except ValueError:
            mod = 0

        add_once = 0
        add_each = mod
        if not self.dice_mod_chk.get_active():
            add_once, add_each = add_each, add_once

        rolls = []
        total = 0
        for _ in range(0, count):
            roll = random.randint(1, die)
            total += roll
            output = str(roll)
            if add_each:
                total += add_each
                output += "+%d (%d)" % (add_each, roll + add_each)
            rolls.append(output)
        total += add_once
        
        self.build_output(die, count, mod, rolls, total)

    def roll_attack(self):
        """Rolls an attack."""
        
        valid = True
        self.num_atks_ent.get_style_context().remove_class("bad-input")
        self.mod_atks_ent.get_style_context().remove_class("bad-input")
        self.crit_atks_ent.get_style_context().remove_class("bad-input")

        # Check validity of the entries.
        num_atks = -1
        try:
            num_atks = int(self.num_atks_ent.get_text())
        except ValueError:
            self.num_atks_ent.get_style_context().add_class("bad-input")
            valid = False

        if num_atks < 1:
            self.num_atks_ent.get_style_context().add_class("bad-input")
            valid = False

        mods = []
        try:
            mods = self.mod_atks_ent.get_text().split(",")
            mods = [x.strip() for x in mods]
            mods = [int(x) for x in mods]
        except ValueError:
            self.mod_atks_ent.get_style_context().add_class("bad-input")
            valid = False

        if len(mods) != num_atks:
            self.num_atks_ent.get_style_context().add_class("bad-input")
            self.mod_atks_ent.get_style_context().add_class("bad-input")
            valid = False

        try:
            crit_range = int(self.crit_atks_ent.get_text())
        except ValueError:
            self.crit_atks_ent.get_style_context().add_class("bad-input")
            crit_range = -1
            valid = False
        
        if crit_range < 0 or crit_range > 20:
            self.crit_atks_ent.get_style_context().add_class("bad-input")
            valid = False
        
        stop_on_crit = self.stop_atks_chk.get_active()

        if not valid:
            return

        rolls = []
        for i in range(0, num_atks):
            roll = random.randint(1, 20)
            rolls.append("Attack %d: %d + %d = <b>%d</b>" % (i + 1, roll, mods[i], roll + mods[i]))
            if roll == 1:
                rolls.append("<span color=\"red\">Critical fail!</span>")
                if stop_on_crit:
                    break
            if roll >= crit_range:
                rolls.append("<span color=\"green\">Critical hit!</span>")
                confirm = random.randint(1, 20)
                rolls.append("Critical confirm: %d + %d = <b>%d</b>" % (confirm, mods[i], confirm + mods[i]))

        self.build_attack_output(num_atks, mods, crit_range, rolls)

    def roll_dmg(self):
        """Rolls damage."""

        valid = True
        self.weap_dam_cbox.get_style_context().remove_class("bad-input")
        self.num_dam_ent.get_style_context().remove_class("bad-input")
        self.mod_dam_ent.get_style_context().remove_class("bad-input")

        # Check validity of the entries.
        weapon_index, weapon_name = -1, ""
        selected_iter = self.weap_dam_cbox.get_active_iter()
        if selected_iter is not None:
            weapon_index, weapon_name = self.weap_dam_store[selected_iter]
        if selected_iter is None or weapon_index == -1:
            self.weap_dam_cbox.get_style_context().add_class("bad-input")
            valid = False

        # Check validity of the entries.
        num_atks = -1
        try:
            num_atks = int(self.num_dam_ent.get_text())
        except ValueError:
            self.num_dam_ent.get_style_context().add_class("bad-input")
            valid = False

        if num_atks < 1:
            self.num_dam_ent.get_style_context().add_class("bad-input")
            valid = False

        mods = []
        try:
            mods = self.mod_dam_ent.get_text().split(",")
            mods = [x.strip() for x in mods]
            mods = [int(x) for x in mods]
        except ValueError:
            self.mod_dam_ent.get_style_context().add_class("bad-input")
            valid = False

        if len(mods) != num_atks:
            self.num_dam_ent.get_style_context().add_class("bad-input")
            self.mod_dam_ent.get_style_context().add_class("bad-input")
            valid = False

        if self.small_dam_rbtn.get_active():
            size = "dmgs"
            count = "counts"
        else:
            size = "dmgm"
            count = "countm"
        crit_attack = self.crit_dam_chk.get_active()

        if not valid:
            return

        weapon = self.weapon_data[weapon_index]
        rolls = []
        total = 0
        for i in range(0, num_atks):
            output = []
            for _ in range(0, weapon[count]):
                roll = random.randint(1, weapon[size])
                output.append(roll)
            rolls.append("Hit %d: %s + %d = <b>%d damage</b>" % (i + 1, " + ".join([str(x) for x in output]),
                                                                 mods[i], sum(output) + mods[i]))
            total += sum(output) + mods[i]

        if crit_attack:
            total *= weapon["critm"]

        self.build_dmg_output(num_atks, mods, weapon_name, rolls, total,
                              crit_attack, weapon["critm"], weapon[size], weapon[count])


# Show the window and start the application.
if __name__ == "__main__" and len(sys.argv) == 1:

    win = DiceRoller()
    win.run()
