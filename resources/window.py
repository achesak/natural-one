# -*- coding: utf-8 -*-
from gi.repository import Gdk, GdkPixbuf, Gtk

from resources.load_images import load_symbolic


class NaturalOneWindow(Gtk.ApplicationWindow):

    def __init__(self, style_css=None, *args, **kwargs):
        super(Gtk.ApplicationWindow, self).__init__(*args, **kwargs)

        self.set_icon_from_file('resources/images/icon128.png')
        self.set_size_request(1000, -1)

        self.results = []

        # Create the header bar.
        self.header = Gtk.HeaderBar()
        self.header.set_title('Dice Roller')
        self.header.set_show_close_button(True)
        self.set_titlebar(self.header)

        # Create the stack.
        self.stack = Gtk.Stack()
        self.stack.set_vexpand(False)
        self.stack.set_hexpand(False)
        self.stack.set_size_request(450, 1)
        self.stack.set_transition_type(
            Gtk.StackTransitionType.SLIDE_LEFT_RIGHT,
        )
        self.stack_switcher = Gtk.StackSwitcher()
        self.stack_switcher.set_stack(self.stack)
        self.header.set_custom_title(self.stack_switcher)
        win_pane = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        win_pane.pack1(self.stack, True, False)
        self.add(win_pane)

        # Create the header buttons.
        self.clear_btn = Gtk.Button()
        self.clear_btn.add(load_symbolic('edit-clear'))
        self.clear_btn.set_tooltip_text('Clear rolls')
        self.header.pack_end(self.clear_btn)

        # Create the Basic grid.
        dice_grid = Gtk.Grid()
        dice_grid.set_row_spacing(18)
        dice_grid.set_column_spacing(12)
        dice_grid.set_border_width(18)

        # Create the dice: d4
        d4_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            'resources/images/d4.png',
            60, 60,
            True,
        )
        d4_img = Gtk.Image.new_from_pixbuf(d4_pixbuf)
        dice_grid.attach(d4_img, 0, 0, 1, 1)
        self.d4_count_ent = Gtk.Entry()
        self.d4_count_ent.set_placeholder_text('1')
        self.d4_count_ent.set_width_chars(4)
        self.d4_count_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.d4_count_ent,
            d4_img,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        d4_d_lbl = Gtk.Label('d4')
        dice_grid.attach_next_to(
            d4_d_lbl,
            self.d4_count_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        d4_plus_lbl = Gtk.Label('+')
        dice_grid.attach_next_to(
            d4_plus_lbl,
            d4_d_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.d4_mod_ent = Gtk.Entry()
        self.d4_mod_ent.set_placeholder_text('0')
        self.d4_mod_ent.set_width_chars(4)
        self.d4_mod_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.d4_mod_ent,
            d4_plus_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.d4_btn = Gtk.Button('Roll')
        dice_grid.attach_next_to(
            self.d4_btn,
            self.d4_mod_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )

        # Create the dice: d6
        d6_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            'resources/images/d6.png',
            60, 60,
            True,
        )
        d6_img = Gtk.Image.new_from_pixbuf(d6_pixbuf)
        dice_grid.attach_next_to(d6_img, d4_img, Gtk.PositionType.BOTTOM, 1, 1)
        self.d6_count_ent = Gtk.Entry()
        self.d6_count_ent.set_placeholder_text('1')
        self.d6_count_ent.set_width_chars(4)
        self.d6_count_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.d6_count_ent,
            d6_img,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        d6_d_lbl = Gtk.Label('d6')
        dice_grid.attach_next_to(
            d6_d_lbl,
            self.d6_count_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        d6_plus_lbl = Gtk.Label('+')
        dice_grid.attach_next_to(
            d6_plus_lbl,
            d6_d_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.d6_mod_ent = Gtk.Entry()
        self.d6_mod_ent.set_placeholder_text('0')
        self.d6_mod_ent.set_width_chars(4)
        self.d6_mod_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.d6_mod_ent,
            d6_plus_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.d6_btn = Gtk.Button('Roll')
        dice_grid.attach_next_to(
            self.d6_btn,
            self.d6_mod_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )

        # Create the dice: d8
        d8_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            'resources/images/d8.png',
            60, 60,
            True,
        )
        d8_img = Gtk.Image.new_from_pixbuf(d8_pixbuf)
        dice_grid.attach_next_to(d8_img, d6_img, Gtk.PositionType.BOTTOM, 1, 1)
        self.d8_count_ent = Gtk.Entry()
        self.d8_count_ent.set_placeholder_text('1')
        self.d8_count_ent.set_width_chars(4)
        self.d8_count_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.d8_count_ent,
            d8_img,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        d8_d_lbl = Gtk.Label('d8')
        dice_grid.attach_next_to(
            d8_d_lbl,
            self.d8_count_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        d8_plus_lbl = Gtk.Label('+')
        dice_grid.attach_next_to(
            d8_plus_lbl,
            d8_d_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.d8_mod_ent = Gtk.Entry()
        self.d8_mod_ent.set_placeholder_text('0')
        self.d8_mod_ent.set_width_chars(4)
        self.d8_mod_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.d8_mod_ent,
            d8_plus_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.d8_btn = Gtk.Button('Roll')
        dice_grid.attach_next_to(
            self.d8_btn,
            self.d8_mod_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )

        # Create the dice: d10
        d10_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            'resources/images/d10.png',
            60, 60,
            True,
        )
        d10_img = Gtk.Image.new_from_pixbuf(d10_pixbuf)
        dice_grid.attach_next_to(
            d10_img,
            d8_img,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.d10_count_ent = Gtk.Entry()
        self.d10_count_ent.set_placeholder_text('1')
        self.d10_count_ent.set_width_chars(4)
        self.d10_count_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.d10_count_ent,
            d10_img,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        d10_d_lbl = Gtk.Label('d10')
        dice_grid.attach_next_to(
            d10_d_lbl,
            self.d10_count_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        d10_plus_lbl = Gtk.Label('+')
        dice_grid.attach_next_to(
            d10_plus_lbl,
            d10_d_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.d10_mod_ent = Gtk.Entry()
        self.d10_mod_ent.set_placeholder_text('0')
        self.d10_mod_ent.set_width_chars(4)
        self.d10_mod_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.d10_mod_ent,
            d10_plus_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.d10_btn = Gtk.Button('Roll')
        dice_grid.attach_next_to(
            self.d10_btn,
            self.d10_mod_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )

        # Create the dice: d12
        d12_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            'resources/images/d12.png',
            60, 60,
            True,
        )
        d12_img = Gtk.Image.new_from_pixbuf(d12_pixbuf)
        dice_grid.attach_next_to(
            d12_img,
            d10_img,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.d12_count_ent = Gtk.Entry()
        self.d12_count_ent.set_placeholder_text('1')
        self.d12_count_ent.set_width_chars(4)
        self.d12_count_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.d12_count_ent,
            d12_img,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        d12_d_lbl = Gtk.Label('d12')
        dice_grid.attach_next_to(
            d12_d_lbl,
            self.d12_count_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        d12_plus_lbl = Gtk.Label('+')
        dice_grid.attach_next_to(
            d12_plus_lbl,
            d12_d_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.d12_mod_ent = Gtk.Entry()
        self.d12_mod_ent.set_placeholder_text('0')
        self.d12_mod_ent.set_width_chars(4)
        self.d12_mod_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.d12_mod_ent,
            d12_plus_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.d12_btn = Gtk.Button('Roll')
        dice_grid.attach_next_to(
            self.d12_btn,
            self.d12_mod_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )

        # Create the dice: d20
        d20_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            'resources/images/d20.png',
            60, 60,
            True,
        )
        d20_img = Gtk.Image.new_from_pixbuf(d20_pixbuf)
        dice_grid.attach_next_to(
            d20_img,
            d12_img,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.d20_count_ent = Gtk.Entry()
        self.d20_count_ent.set_placeholder_text('1')
        self.d20_count_ent.set_width_chars(4)
        self.d20_count_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.d20_count_ent,
            d20_img,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        d20_d_lbl = Gtk.Label('d20')
        dice_grid.attach_next_to(
            d20_d_lbl,
            self.d20_count_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        d20_plus_lbl = Gtk.Label('+')
        dice_grid.attach_next_to(
            d20_plus_lbl,
            d20_d_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.d20_mod_ent = Gtk.Entry()
        self.d20_mod_ent.set_placeholder_text('0')
        self.d20_mod_ent.set_width_chars(4)
        self.d20_mod_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.d20_mod_ent,
            d20_plus_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.d20_btn = Gtk.Button('Roll')
        dice_grid.attach_next_to(
            self.d20_btn,
            self.d20_mod_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )

        # Create the dice: custom
        dq_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            'resources/images/general.png',
            60, 60,
            True,
        )
        dq_img = Gtk.Image.new_from_pixbuf(dq_pixbuf)
        dice_grid.attach_next_to(
            dq_img,
            d20_img,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.dq_count_ent = Gtk.Entry()
        self.dq_count_ent.set_placeholder_text('1')
        self.dq_count_ent.set_width_chars(4)
        self.dq_count_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.dq_count_ent,
            dq_img,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        dq_box = Gtk.Box()
        dq_d_lbl = Gtk.Label('d')
        dq_d_lbl.set_alignment(1, 0.5)
        dq_box.add(dq_d_lbl)
        self.dq_size_ent = Gtk.Entry()
        self.dq_size_ent.set_width_chars(4)
        self.dq_size_ent.props.xalign = 0.5
        self.dq_size_ent.set_margin_left(5)
        self.dq_error_popover = Gtk.Popover()
        self.dq_error_popover.set_relative_to(self.dq_size_ent)
        dq_box.add(self.dq_size_ent)
        dice_grid.attach_next_to(
            dq_box,
            self.dq_count_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        dq_plus_lbl = Gtk.Label('+')
        dice_grid.attach_next_to(
            dq_plus_lbl,
            dq_box,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.dq_mod_ent = Gtk.Entry()
        self.dq_mod_ent.set_placeholder_text('0')
        self.dq_mod_ent.set_width_chars(4)
        self.dq_mod_ent.props.xalign = 0.5
        dice_grid.attach_next_to(
            self.dq_mod_ent,
            dq_plus_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.dq_btn = Gtk.Button('Roll')
        dice_grid.attach_next_to(
            self.dq_btn,
            self.dq_mod_ent,
            Gtk.PositionType.RIGHT,
            1, 1,
        )

        # Create the minimum value entry.
        min_value_lbl = Gtk.Label('Minimum value')
        min_value_lbl.set_alignment(1, 0.5)
        dice_grid.attach_next_to(
            min_value_lbl,
            dq_img,
            Gtk.PositionType.BOTTOM,
            2, 1,
        )
        self.min_value_ent = Gtk.Entry()
        self.min_value_ent.set_placeholder_text('No minimum value')
        dice_grid.attach_next_to(
            self.min_value_ent,
            min_value_lbl,
            Gtk.PositionType.RIGHT,
            4, 1,
        )

        # Create the modifier check box.
        self.dice_mod_chk = Gtk.CheckButton('Add modifier to every roll')
        self.dice_mod_chk.set_active(True)
        self.dice_mod_chk.set_halign(Gtk.Align.CENTER)
        self.dice_mod_chk.set_hexpand(True)
        dice_grid.attach_next_to(
            self.dice_mod_chk,
            min_value_lbl,
            Gtk.PositionType.BOTTOM,
            6, 1,
        )

        # Create the Combat grid.
        combat_grid = Gtk.Grid()
        combat_grid.set_row_spacing(5)
        combat_grid.set_column_spacing(12)
        combat_grid.set_border_width(18)

        # Create the attack roll main label.
        atk_lbl = Gtk.Label()
        atk_lbl.set_markup('<span size="x-large">Attack Roll</span>')
        atk_lbl.set_alignment(0, 0.5)
        combat_grid.add(atk_lbl)

        # Create the number of attacks row.
        num_atks_lbl = Gtk.Label('Number of attacks')
        num_atks_lbl.set_alignment(1, 0.5)
        combat_grid.attach_next_to(
            num_atks_lbl,
            atk_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.num_atks_ent = Gtk.Entry()
        self.num_atks_ent.set_hexpand(True)
        self.num_atks_ent.set_placeholder_text('1')
        combat_grid.attach_next_to(
            self.num_atks_ent,
            num_atks_lbl,
            Gtk.PositionType.RIGHT,
            3, 1,
        )

        # Create the modifiers row.
        mod_atks_lbl = Gtk.Label('Modifiers')
        mod_atks_lbl.set_alignment(1, 0.5)
        combat_grid.attach_next_to(
            mod_atks_lbl,
            num_atks_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.mod_atks_ent = Gtk.Entry()
        self.mod_atks_ent.set_hexpand(True)
        self.mod_atks_ent.set_placeholder_text('0')
        combat_grid.attach_next_to(
            self.mod_atks_ent,
            mod_atks_lbl,
            Gtk.PositionType.RIGHT,
            3, 1,
        )

        # Create the critical range row.
        crit_atks_lbl = Gtk.Label('Critical range')
        crit_atks_lbl.set_alignment(1, 0.5)
        combat_grid.attach_next_to(
            crit_atks_lbl,
            mod_atks_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        crit_atks_box = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        self.crit_atks_ent = Gtk.Entry()
        self.crit_atks_ent.set_hexpand(True)
        self.crit_atks_ent.set_placeholder_text('20')
        crit_20_atks_lbl = Gtk.Label('- 20')
        crit_20_atks_lbl.set_alignment(1, 0.5)
        crit_20_atks_lbl.set_margin_left(5)
        crit_atks_box.pack_start(self.crit_atks_ent, True, True, 0)
        crit_atks_box.pack_start(crit_20_atks_lbl, False, False, 0)
        combat_grid.attach_next_to(
            crit_atks_box,
            crit_atks_lbl,
            Gtk.PositionType.RIGHT,
            3, 1,
        )

        # Create the confirm critical row.
        self.confirm_atks_chk = Gtk.CheckButton('Confirm critical hits')
        self.confirm_atks_chk.set_active(True)
        combat_grid.attach_next_to(
            self.confirm_atks_chk,
            crit_atks_lbl,
            Gtk.PositionType.BOTTOM,
            2, 1,
        )

        # Create the stop on fail row.
        self.stop_atks_chk = Gtk.CheckButton('Stop on critical fail')
        self.stop_atks_chk.set_active(True)
        combat_grid.attach_next_to(
            self.stop_atks_chk,
            self.confirm_atks_chk,
            Gtk.PositionType.BOTTOM,
            2, 1,
        )

        # Create the attack roll button.
        self.atk_btn = Gtk.Button('Roll')
        combat_grid.attach_next_to(
            self.atk_btn,
            self.stop_atks_chk,
            Gtk.PositionType.RIGHT,
            2, 1,
        )

        # Create the damage roll main label.
        dam_lbl = Gtk.Label()
        dam_lbl.set_markup('<span size="x-large">Damage Roll</span>')
        dam_lbl.set_alignment(0, 0.5)
        dam_lbl.set_margin_top(15)
        combat_grid.attach_next_to(
            dam_lbl,
            self.stop_atks_chk,
            Gtk.PositionType.BOTTOM,
            4, 1,
        )

        # Create the system row.
        sys_dam_lbl = Gtk.Label('System')
        sys_dam_lbl.set_alignment(1, 0.5)
        combat_grid.attach_next_to(
            sys_dam_lbl,
            dam_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        sys_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        sys_btn_box.set_hexpand(True)
        Gtk.StyleContext.add_class(sys_btn_box.get_style_context(), 'linked')
        self.sys_dam_cbox = Gtk.ComboBoxText.new()
        self.sys_dam_cbox.set_hexpand(True)
        sys_btn_box.add(self.sys_dam_cbox)
        self.sys_manage_btn = Gtk.Button()
        self.sys_manage_btn.add(load_symbolic('document-properties'))
        self.sys_manage_btn.set_tooltip_text('Add and manage systems')
        sys_btn_box.add(self.sys_manage_btn)
        combat_grid.attach_next_to(
            sys_btn_box,
            sys_dam_lbl,
            Gtk.PositionType.RIGHT,
            3, 1,
        )

        # Create the weapon row.
        dam_scroll_win = Gtk.ScrolledWindow()
        dam_scroll_win.set_hexpand(True)
        dam_scroll_win.set_vexpand(True)
        self.weap_dam_store = Gtk.TreeStore(str)
        self.weap_dam_tree = Gtk.TreeView()
        self.weap_dam_tree.set_model(self.weap_dam_store)
        self.weap_dam_tree.set_headers_visible(False)
        dam_scroll_win.add(self.weap_dam_tree)
        weap_dam_crend = Gtk.CellRendererText()
        weap_dam_col = Gtk.TreeViewColumn('Weapons', weap_dam_crend, text=0)
        self.weap_dam_tree.append_column(weap_dam_col)
        combat_grid.attach_next_to(
            dam_scroll_win,
            sys_dam_lbl,
            Gtk.PositionType.BOTTOM,
            4, 1,
        )
        self.weap_error_popover = Gtk.Popover()
        self.weap_error_popover.set_relative_to(self.weap_dam_tree)

        # Create the number of attacks row.
        num_dam_lbl = Gtk.Label('Number of attacks')
        num_dam_lbl.set_alignment(1, 0.5)
        combat_grid.attach_next_to(
            num_dam_lbl,
            dam_scroll_win,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.num_dam_ent = Gtk.Entry()
        self.num_dam_ent.set_hexpand(True)
        self.num_dam_ent.set_placeholder_text('1')
        combat_grid.attach_next_to(
            self.num_dam_ent,
            num_dam_lbl,
            Gtk.PositionType.RIGHT,
            3, 1,
        )

        # Create the damage modifier row.
        mod_dam_lbl = Gtk.Label('Modifiers')
        mod_dam_lbl.set_alignment(1, 0.5)
        combat_grid.attach_next_to(
            mod_dam_lbl,
            num_dam_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.mod_dam_ent = Gtk.Entry()
        self.mod_dam_ent.set_hexpand(True)
        self.mod_dam_ent.set_placeholder_text('0')
        combat_grid.attach_next_to(
            self.mod_dam_ent,
            mod_dam_lbl,
            Gtk.PositionType.RIGHT,
            3, 1,
        )

        # Create the minimum value row.
        min_dam_lbl = Gtk.Label('Minimum value')
        min_dam_lbl.set_alignment(1, 0.5)
        combat_grid.attach_next_to(
            min_dam_lbl,
            mod_dam_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.min_dam_ent = Gtk.Entry()
        self.min_dam_ent.set_hexpand(True)
        self.min_dam_ent.set_placeholder_text('No minimum value')
        combat_grid.attach_next_to(
            self.min_dam_ent,
            min_dam_lbl,
            Gtk.PositionType.RIGHT,
            3, 1,
        )

        # Create the size row.
        size_combat_grid = Gtk.Grid()
        size_combat_grid.set_column_spacing(15)
        self.small_dam_rbtn = Gtk.RadioButton.new_with_label_from_widget(
            None,
            'Small',
        )
        self.med_dam_rbtn = Gtk.RadioButton.new_with_label_from_widget(
            self.small_dam_rbtn,
            'Medium',
        )
        self.med_dam_rbtn.set_active(True)
        size_combat_grid.add(self.small_dam_rbtn)
        size_combat_grid.attach_next_to(
            self.med_dam_rbtn,
            self.small_dam_rbtn,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        combat_grid.attach_next_to(
            size_combat_grid,
            min_dam_lbl,
            Gtk.PositionType.BOTTOM,
            3, 1,
        )

        # Create the critical row.
        self.crit_dam_chk = Gtk.CheckButton('Critical hit')
        combat_grid.attach_next_to(
            self.crit_dam_chk,
            size_combat_grid,
            Gtk.PositionType.BOTTOM,
            2, 1,
        )

        # Create the damage roll button.
        self.dam_btn = Gtk.Button('Roll')
        combat_grid.attach_next_to(
            self.dam_btn,
            self.crit_dam_chk,
            Gtk.PositionType.RIGHT,
            2, 1,
        )

        # Create the Templates grid.
        templates_grid = Gtk.Grid()
        templates_grid.set_row_spacing(0)
        templates_grid.set_column_spacing(12)
        templates_grid.set_border_width(18)

        # Create the template list main label.
        list_lbl = Gtk.Label()
        list_lbl.set_markup('<span size="x-large">Templates</span>')
        list_lbl.set_alignment(0, 0.5)
        list_lbl.set_margin_bottom(10)
        templates_grid.add(list_lbl)

        # Create the template list.
        templates_scroll_win = Gtk.ScrolledWindow()
        templates_scroll_win.set_hexpand(True)
        templates_scroll_win.set_vexpand(True)
        templates_grid.attach_next_to(
            templates_scroll_win,
            list_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.template_store = Gtk.ListStore(int, str, int)
        self.template_tree = Gtk.TreeView(model=self.template_store)
        self.template_tree.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.template_tree.set_reorderable(True)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Name', renderer, text=1)
        column.set_expand(True)
        self.template_tree.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Rolls', renderer, text=2)
        self.template_tree.append_column(column)
        templates_scroll_win.add(self.template_tree)

        # Create the template list action bar.
        self.template_action_bar = Gtk.ActionBar()
        templates_grid.attach_next_to(
            self.template_action_bar,
            templates_scroll_win,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )

        # Create the template list buttons.
        template_edit_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(
            template_edit_btn_box.get_style_context(),
            'linked',
        )
        self.template_action_bar.pack_start(template_edit_btn_box)
        self.new_btn = Gtk.Button()
        self.new_btn.add(load_symbolic('list-add'))
        self.new_btn.set_tooltip_text('Create a new template')
        template_edit_btn_box.add(self.new_btn)
        self.list_edit_btn = Gtk.Button()
        self.list_edit_btn.add(load_symbolic('edit'))
        self.list_edit_btn.set_tooltip_text('Edit selected template')
        template_edit_btn_box.add(self.list_edit_btn)
        self.list_delete_btn = Gtk.Button()
        self.list_delete_btn.add(load_symbolic('list-remove'))
        self.list_delete_btn.set_tooltip_text('Delete selected template')
        template_edit_btn_box.add(self.list_delete_btn)
        template_file_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(
            template_file_btn_box.get_style_context(),
            'linked',
        )
        self.template_action_bar.pack_start(template_file_btn_box)
        self.list_save_btn = Gtk.Button()
        self.list_save_btn.add(load_symbolic('document-save'))
        self.list_save_btn.set_tooltip_text('Export templates')
        template_file_btn_box.add(self.list_save_btn)
        self.list_open_btn = Gtk.Button()
        self.list_open_btn.add(load_symbolic('document-open'))
        self.list_open_btn.set_tooltip_text('Import templates')
        template_file_btn_box.add(self.list_open_btn)
        self.list_roll_btn = Gtk.Button()
        self.list_roll_btn.add(load_symbolic('go-jump'))
        self.list_roll_btn.set_tooltip_text('Roll selected template')
        self.template_action_bar.pack_end(self.list_roll_btn)

        # Create the template list critical check box.
        self.list_crit_chk = Gtk.CheckButton('Apply critical hit')
        self.list_crit_chk.set_halign(Gtk.Align.CENTER)
        self.list_crit_chk.set_hexpand(True)
        self.list_crit_chk.set_margin_top(10)
        templates_grid.attach_next_to(
            self.list_crit_chk,
            self.template_action_bar,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )

        # Create the template drag and drop help text.
        drag_list_lbl = Gtk.Label(
            'Drag and drop to rearrange templates',
        )
        drag_list_lbl.set_margin_top(10)
        templates_grid.attach_next_to(
            drag_list_lbl,
            self.list_crit_chk,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )

        # Create the Initiative grid.
        init_grid = Gtk.Grid()
        init_grid.set_row_spacing(18)
        init_grid.set_column_spacing(12)
        init_grid.set_border_width(18)

        # Create the add initiative grid.
        add_init_grid = Gtk.Grid()
        add_init_grid.set_row_spacing(5)
        add_init_grid.set_column_spacing(12)
        init_grid.add(add_init_grid)

        # Create the add initiative label.
        add_init_lbl = Gtk.Label()
        add_init_lbl.set_markup('<span size="x-large">Add Initiative</span>')
        add_init_lbl.set_alignment(0, 0.5)
        add_init_grid.attach(add_init_lbl, 0, 0, 1, 1)

        # Create the initiative mode box.
        mode_init_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        mode_init_box.set_margin_top(5)
        mode_init_box.props.halign = Gtk.Align.CENTER
        add_init_grid.attach_next_to(
            mode_init_box,
            add_init_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )

        # Create the initiative mode radiobuttons.
        self.roll_init_rbtn = Gtk.RadioButton.new_with_label_from_widget(
            None,
            'Roll initiative',
        )
        self.roll_init_rbtn.set_margin_left(10)
        self.add_init_rbtn = Gtk.RadioButton.new_with_label_from_widget(
            self.roll_init_rbtn,
            'Add initiative directly',
        )
        mode_init_box.pack_start(self.roll_init_rbtn, False, False, 0)
        mode_init_box.pack_start(self.add_init_rbtn, False, False, 0)

        # Create the roll initiative grid.
        roll_init_grid = Gtk.Grid()
        roll_init_grid.set_row_spacing(5)
        roll_init_grid.set_column_spacing(12)
        add_init_grid.attach_next_to(
            roll_init_grid,
            mode_init_box,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )

        # Create the name label and entry.
        name_init_lbl = Gtk.Label('Name')
        name_init_lbl.set_alignment(1, 0.5)
        roll_init_grid.attach(name_init_lbl, 0, 0, 1, 1)
        self.name_init_ent = Gtk.Entry()
        self.name_init_ent.set_hexpand(True)
        roll_init_grid.attach_next_to(
            self.name_init_ent,
            name_init_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )
        self.name_init_error_popover = Gtk.Popover()
        self.name_init_error_popover.set_relative_to(self.name_init_ent)

        # Create the modifier label and entry.
        self.mod_init_lbl = Gtk.Label('Modifier')
        self.mod_init_lbl.set_alignment(1, 0.5)
        roll_init_grid.attach_next_to(
            self.mod_init_lbl,
            name_init_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        mod_init_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(mod_init_box.get_style_context(), 'linked')
        self.mod_init_ent = Gtk.Entry()
        self.mod_init_ent.set_hexpand(True)
        self.mod_init_ent.set_placeholder_text('0')
        mod_init_box.add(self.mod_init_ent)
        self.roll_init_btn = Gtk.Button('Roll')
        mod_init_box.add(self.roll_init_btn)
        roll_init_grid.attach_next_to(
            mod_init_box,
            self.mod_init_lbl,
            Gtk.PositionType.RIGHT,
            1, 1,
        )

        # Create the sorting check box.
        self.sort_init_chk = Gtk.CheckButton('Automatically sort initiatives')
        self.sort_init_chk.set_halign(Gtk.Align.CENTER)
        self.sort_init_chk.set_hexpand(True)
        self.sort_init_chk.set_margin_top(5)
        self.sort_init_chk.set_active(True)
        add_init_grid.attach_next_to(
            self.sort_init_chk,
            roll_init_grid,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )

        # Create the initiative list grid.
        list_init_grid = Gtk.Grid()
        list_init_grid.set_row_spacing(0)
        list_init_grid.set_column_spacing(12)
        init_grid.attach_next_to(
            list_init_grid,
            add_init_grid,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )

        # Create the initiative list label.
        list_init_lbl = Gtk.Label()
        list_init_lbl.set_markup('<span size="x-large">Initiative List</span>')
        list_init_lbl.set_alignment(0, 0.5)
        list_init_lbl.set_margin_bottom(10)
        list_init_grid.attach(list_init_lbl, 0, 0, 1, 1)

        # Create the initiative list.
        init_scroll_win = Gtk.ScrolledWindow()
        init_scroll_win.set_hexpand(True)
        init_scroll_win.set_vexpand(True)
        list_init_grid.attach_next_to(
            init_scroll_win,
            list_init_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.init_store = Gtk.ListStore(int, str, int)
        self.init_tree = Gtk.TreeView(model=self.init_store)
        self.init_tree.set_reorderable(True)
        self.init_tree.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Name', renderer, text=1)
        column.set_expand(True)
        self.init_tree.append_column(column)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Initiative', renderer, text=2)
        self.init_tree.append_column(column)
        init_scroll_win.add(self.init_tree)

        # Create the initiative list action bar.
        self.init_action_bar = Gtk.ActionBar()
        list_init_grid.attach_next_to(
            self.init_action_bar,
            init_scroll_win,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )

        # Create the initiative list buttons.
        init_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(init_btn_box.get_style_context(), 'linked')
        self.init_action_bar.pack_start(init_btn_box)
        self.remove_init_btn = Gtk.Button()
        self.remove_init_btn.add(load_symbolic('list-remove'))
        self.remove_init_btn.set_tooltip_text('Remove selected initiative')
        init_btn_box.add(self.remove_init_btn)
        self.clear_init_btn = Gtk.Button()
        self.clear_init_btn.add(load_symbolic('edit-clear'))
        self.clear_init_btn.set_tooltip_text('Clear all initiatives')
        init_btn_box.add(self.clear_init_btn)

        # Create the initiative drag and drop help text.
        drag_init_lbl = Gtk.Label(
            'Drag and drop to rearrange initiative order',
        )
        drag_init_lbl.set_margin_top(10)
        list_init_grid.attach_next_to(
            drag_init_lbl,
            self.init_action_bar,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )

        # Create the results display.
        self.results_scroll_win = Gtk.ScrolledWindow()
        self.results_scroll_win.set_hexpand(True)
        self.results_scroll_win.set_vexpand(True)
        self.results_scroll_win.set_size_request(550, -1)
        self.results_store = Gtk.ListStore(str)
        self.results_tree = Gtk.TreeView(model=self.results_store)
        self.results_tree.set_headers_visible(False)
        renderer = Gtk.CellRendererText()
        renderer.set_padding(12, 12)
        column = Gtk.TreeViewColumn('Name', renderer, markup=0)
        column.set_expand(True)
        column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.results_tree.append_column(column)
        self.results_scroll_win.add(self.results_tree)
        win_pane.pack2(self.results_scroll_win, True, True)

        # Create the CSS provider.
        self.style_provider = Gtk.CssProvider()
        self.style_context = Gtk.StyleContext()
        self.style_context.add_provider_for_screen(
            Gdk.Screen.get_default(),
            self.style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
        self.style_provider.load_from_data(style_css)

        # Set up the stack.
        self.stack.add_titled(dice_grid, 'basic', 'Basic')
        self.stack.add_titled(combat_grid, 'combat', 'Combat')
        self.stack.add_titled(templates_grid, 'templates', 'Templates')
        self.stack.add_titled(init_grid, 'initiative', 'Initiatives')

    @staticmethod
    def add_error(widget):
        widget.get_style_context().add_class('bad-input')

    @staticmethod
    def remove_error(widget):
        widget.get_style_context().remove_class('bad-input')

    @staticmethod
    def show_popup(widget, message='', required=True):
        children = widget.get_children()
        for child in children:
            child.destroy()

        if required:
            if message:
                message = 'Required: ' + message[0].lower() + message[1:]
            else:
                message = 'Required'

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        error_img = load_symbolic('dialog-error')
        error_img.set_margin_top(10)
        error_img.set_margin_bottom(10)
        error_img.set_margin_left(10)
        error_img.set_margin_right(5)
        box.pack_start(error_img, False, False, 0)

        message_lbl = Gtk.Label(message)
        message_lbl.set_margin_top(10)
        message_lbl.set_margin_bottom(10)
        message_lbl.set_margin_right(10)
        box.pack_end(message_lbl, True, True, 0)

        widget.add(box)
        widget.show_all()
        widget.popup()

    def remove_errors(self):
        widgets = [
            self.d4_count_ent, self.d4_mod_ent, self.d6_count_ent,
            self.d6_mod_ent, self.d8_count_ent, self.d8_mod_ent,
            self.d10_count_ent, self.d10_mod_ent, self.d12_count_ent,
            self.d12_mod_ent, self.d20_count_ent, self.d20_mod_ent,
            self.dq_size_ent, self.dq_count_ent, self.dq_mod_ent,
            self.min_value_ent, self.num_atks_ent, self.mod_atks_ent,
            self.crit_atks_ent, self.weap_dam_tree, self.num_dam_ent,
            self.mod_dam_ent, self.min_dam_ent, self.name_init_ent,
            self.mod_init_ent,
        ]

        for widget in widgets:
            self.remove_error(widget)

    def update_output(self, new_text):
        self.results.insert(0, [new_text])

        self.results_store.clear()
        for result in self.results:
            self.results_store.append(result)

        self.results_scroll_win.get_vadjustment().set_value(0)

    def clear_output(self):
        self.results = []
        self.results_store.clear()

    def toggle_initiative_mode(self):
        roll_is_active = self.roll_init_rbtn.get_active()

        if roll_is_active:
            self.mod_init_lbl.set_text('Modifier')
            self.roll_init_btn.set_label('Roll')

        else:
            self.mod_init_lbl.set_text('Initiative')
            self.roll_init_btn.set_label('Add')

    @staticmethod
    def limit_number_input(
            widget,
            allow_negative=True,
            allow_comma=False,
            allow_whitespace=False,
            max_limit=None,
    ):
        allowed = '0123456789'
        if allow_negative:
            allowed += '-'
        if allow_comma:
            allowed += ','
        if allow_whitespace:
            allowed += ' \t'

        text = widget.get_text()
        filtered_text = ''.join([char for char in text if char in allowed])
        if not allow_comma and not allow_whitespace and filtered_text:
            suffix = filtered_text[1:]
            suffix = ''.join([char for char in suffix if char != '-'])
            filtered_text = filtered_text[0] + suffix

        try:
            if max_limit is not None and int(filtered_text) > max_limit:
                filtered_text = str(max_limit)
        except ValueError:
            pass

        widget.set_text(filtered_text)

    def register_limit_inputs(self):
        number_inputs = [
            self.d4_mod_ent, self.d6_mod_ent, self.d8_mod_ent,
            self.d10_mod_ent, self.d12_mod_ent, self.d20_mod_ent,
            self.dq_mod_ent, self.min_value_ent, self.min_dam_ent,
            self.mod_init_ent,
        ]
        count_inputs = [
            self.d4_count_ent, self.d6_count_ent, self.d8_count_ent,
            self.d10_count_ent, self.d12_count_ent, self.d20_count_ent,
            self.dq_mod_ent, self.dq_size_ent, self.num_atks_ent,
            self.num_dam_ent,
        ]
        mod_inputs = [
            self.mod_atks_ent, self.mod_dam_ent,
        ]

        for limited_imput in number_inputs:
            limited_imput.connect('changed', self.limit_number_input)

        for limited_imput in count_inputs:
            limited_imput.connect(
                'changed',
                lambda limited_input=limited_imput: self.limit_number_input(
                    limited_input,
                    allow_negative=False,
                ),
            )

        for limited_imput in mod_inputs:
            limited_imput.connect(
                'changed',
                lambda limited_input=limited_imput: self.limit_number_input(
                    limited_input,
                    allow_comma=True,
                    allow_whitespace=True,
                ),
            )

        self.crit_atks_ent.connect(
            'changed',
            lambda limited_input: self.limit_number_input(
                limited_input,
                allow_negative=False,
                max_limit=20,
            ),
        )

    @staticmethod
    def int_or(widget, default):
        try:
            return int(widget.get_text().strip())
        except ValueError:
            return default

    @staticmethod
    def mods_or(widget, default):
        try:
            mods = widget.get_text().split(',')
            mods = [x.strip() for x in mods]
            mods = [int(x) for x in mods]
            return mods
        except ValueError:
            return default

    @staticmethod
    def get_selected_index(widget):
        model, treeiter = widget.get_selection().get_selected_rows()
        index = None
        for i in treeiter:
            index = int(str(i))

        return index

    @staticmethod
    def get_selected_indices(widget):
        model, treeiter = widget.get_selection().get_selected_rows()
        indices = []
        for i in treeiter:
            indices.append(int(str(i)))

        return indices
