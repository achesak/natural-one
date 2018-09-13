# -*- coding: utf-8 -*-
import copy

from gi.repository import Gdk, Gtk

from resources.constants import CriticalOptions, CRITICAL_OPTIONS
from resources.dialogs.generic_dialogs import show_question
from resources.load_images import load_symbolic
from resources.utility import pluralize, pluralize_adj, sign
from resources.window import NaturalOneWindow


class TemplateDialog(Gtk.Dialog):

    def __init__(
            self,
            parent,
            subtitle,
            name=None,
            rolls=None,
            style_css=None
    ):

        if rolls is None:
            rolls = []
        self.rolls = copy.deepcopy(rolls)
        self.name = name

        Gtk.Dialog.__init__(
            self,
            'Template',
            parent,
            Gtk.DialogFlags.MODAL,
            use_header_bar=True,
        )
        self.set_size_request(600, 900)
        self.add_button('Cancel', Gtk.ResponseType.CANCEL)
        self.add_button('OK', Gtk.ResponseType.OK)

        # Create the header bar.
        header = self.get_header_bar()
        header.set_title('Template')
        header.set_subtitle(subtitle)

        # Create the main grid.
        dlg_grid = Gtk.Grid()
        dlg_grid.set_row_spacing(18)
        dlg_grid.set_column_spacing(12)
        dlg_grid.set_border_width(18)
        self.get_content_area().add(dlg_grid)

        # Create the add roll grid.
        add_grid = Gtk.Grid()
        add_grid.set_row_spacing(8)
        add_grid.set_column_spacing(12)
        dlg_grid.attach(add_grid, 0, 0, 1, 1)

        # Create the template details main label.
        details_lbl = Gtk.Label()
        details_lbl.set_markup(
            '<span size="x-large">Template Details</span>',
        )
        details_lbl.set_alignment(0, 0.5)
        details_lbl.set_margin_bottom(5)
        add_grid.attach_next_to(
            details_lbl,
            None,
            Gtk.PositionType.RIGHT,
            3, 1,
        )

        # Create the template name row.
        name_lbl = Gtk.Label('Name')
        name_lbl.set_alignment(1, 0.5)
        add_grid.attach_next_to(
            name_lbl,
            details_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.name_ent = Gtk.Entry()
        self.name_ent.set_hexpand(True)
        add_grid.attach_next_to(
            self.name_ent,
            name_lbl,
            Gtk.PositionType.RIGHT,
            2, 1,
        )

        # Create the add roll main label.
        add_lbl = Gtk.Label()
        add_lbl.set_markup('<span size=\'x-large\'>Add Roll</span>')
        add_lbl.set_alignment(0, 0.5)
        add_lbl.set_margin_top(5)
        add_lbl.set_margin_bottom(5)
        add_grid.attach_next_to(
            add_lbl,
            name_lbl,
            Gtk.PositionType.BOTTOM,
            3, 1,
        )

        # Create the roll row.
        roll_row_lbl = Gtk.Label('Roll')
        roll_row_lbl.set_alignment(1, 0.5)
        add_grid.attach_next_to(
            roll_row_lbl,
            add_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        roll_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.count_ent = Gtk.Entry()
        self.count_ent.set_width_chars(4)
        self.count_ent.props.xalign = 0.5
        roll_box.pack_start(self.count_ent, False, False, 0)
        self.count_error_popover = Gtk.Popover()
        self.count_error_popover.set_relative_to(self.count_ent)
        d_lbl = Gtk.Label('d')
        roll_box.pack_start(d_lbl, True, True, 0)
        self.die_ent = Gtk.Entry()
        self.die_ent.set_width_chars(4)
        self.die_ent.props.xalign = 0.5
        roll_box.pack_start(self.die_ent, False, False, 0)
        self.die_error_popover = Gtk.Popover()
        self.die_error_popover.set_relative_to(self.die_ent)
        plus_lbl = Gtk.Label('+')
        roll_box.pack_start(plus_lbl, True, True, 0)
        self.mod_ent = Gtk.Entry()
        self.mod_ent.set_width_chars(4)
        self.mod_ent.props.xalign = 0.5
        roll_box.pack_start(self.mod_ent, False, False, 0)
        self.mod_error_popover = Gtk.Popover()
        self.mod_error_popover.set_relative_to(self.mod_ent)
        self.mod_chk = Gtk.CheckButton('Add modifier to every roll')
        self.mod_chk.set_active(True)
        self.mod_chk.set_margin_left(12)
        roll_box.pack_start(self.mod_chk, False, False, 0)
        add_grid.attach_next_to(
            roll_box,
            roll_row_lbl,
            Gtk.PositionType.RIGHT,
            2, 1,
        )

        # Create the critical row.
        crit_lbl = Gtk.Label('On critical')
        crit_lbl.set_alignment(1, 0.5)
        crit_store = Gtk.ListStore(str, int)
        for crit_option in CRITICAL_OPTIONS:
            crit_store.append(crit_option)
        self.crit_cbox = Gtk.ComboBox.new_with_model(crit_store)
        self.crit_cbox.set_active(0)
        crit_renderer = Gtk.CellRendererText()
        self.crit_cbox.pack_start(crit_renderer, True)
        self.crit_cbox.add_attribute(crit_renderer, 'text', 0)
        add_grid.attach_next_to(
            crit_lbl,
            roll_row_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        add_grid.attach_next_to(
            self.crit_cbox,
            crit_lbl,
            Gtk.PositionType.RIGHT,
            2, 1,
        )

        # Create the critical multiplier row.
        crit_placeholder_lbl = Gtk.Label('')
        crit_mult_lbl = Gtk.Label('Multiplier')
        crit_mult_lbl.set_margin_right(12)
        self.crit_ent = Gtk.Entry()
        self.crit_ent.set_width_chars(4)
        self.crit_ent.props.xalign = 0.5
        crit_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.crit_error_popover = Gtk.Popover()
        self.crit_error_popover.set_relative_to(self.crit_ent)
        crit_box.pack_start(crit_mult_lbl, False, False, 0)
        crit_box.pack_start(self.crit_ent, False, False, 0)
        add_grid.attach_next_to(
            crit_placeholder_lbl,
            crit_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        add_grid.attach_next_to(
            crit_box,
            crit_placeholder_lbl,
            Gtk.PositionType.RIGHT,
            2, 1,
        )

        # Create the minimum value row.
        min_value_lbl = Gtk.Label('Minimum value')
        min_value_lbl.set_alignment(1, 0.5)
        self.min_value_ent = Gtk.Entry()
        self.min_value_ent.set_placeholder_text('No minimum value')
        self.min_value_ent.set_hexpand(True)
        add_grid.attach_next_to(
            min_value_lbl,
            crit_placeholder_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        add_grid.attach_next_to(
            self.min_value_ent,
            min_value_lbl,
            Gtk.PositionType.RIGHT,
            2, 1,
        )

        # Create the description row.
        desc_lbl = Gtk.Label('Name')
        desc_lbl.set_alignment(1, 0.5)
        desc_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(desc_box.get_style_context(), 'linked')
        self.desc_ent = Gtk.Entry()
        self.desc_ent.set_hexpand(True)
        desc_box.add(self.desc_ent)
        self.desc_error_popover = Gtk.Popover()
        self.desc_error_popover.set_relative_to(self.desc_ent)
        self.add_btn = Gtk.Button('Add Roll')
        desc_box.add(self.add_btn)
        add_grid.attach_next_to(
            desc_lbl,
            min_value_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        add_grid.attach_next_to(
            desc_box,
            desc_lbl,
            Gtk.PositionType.RIGHT,
            2, 1,
        )

        # Create the rolls grid.
        roll_grid = Gtk.Grid()
        roll_grid.set_row_spacing(0)
        roll_grid.set_column_spacing(12)
        dlg_grid.attach(roll_grid, 0, 1, 1, 1)

        # Create the rolls main label.
        roll_lbl = Gtk.Label()
        roll_lbl.set_markup('<span size=\'x-large\'>Rolls</span>')
        roll_lbl.set_alignment(0, 0.5)
        roll_lbl.set_margin_bottom(10)
        roll_grid.attach_next_to(roll_lbl, None, Gtk.PositionType.RIGHT, 1, 1)

        # Create the rolls list.
        roll_scroll_win = Gtk.ScrolledWindow()
        roll_scroll_win.set_hexpand(True)
        roll_scroll_win.set_vexpand(True)
        roll_grid.attach_next_to(
            roll_scroll_win,
            roll_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.roll_store = Gtk.ListStore(int, str, str, str)
        self.roll_tree = Gtk.TreeView(model=self.roll_store)
        self.roll_tree.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.roll_tree.set_reorderable(True)
        desc_text = Gtk.CellRendererText()
        desc_text.set_padding(5, 5)
        self.desc_col = Gtk.TreeViewColumn('Name', desc_text, text=1)
        self.desc_col.set_expand(True)
        self.roll_tree.append_column(self.desc_col)
        roll_text = Gtk.CellRendererText()
        roll_text.set_padding(5, 5)
        self.roll_col = Gtk.TreeViewColumn('Roll', roll_text, text=2)
        self.roll_col.set_expand(True)
        self.roll_tree.append_column(self.roll_col)
        crit_text = Gtk.CellRendererText()
        crit_text.set_padding(5, 5)
        self.crit_col = Gtk.TreeViewColumn('Critical', crit_text, text=3)
        self.crit_col.set_expand(True)
        self.roll_tree.append_column(self.crit_col)
        roll_scroll_win.add(self.roll_tree)

        # Create the roll list action bar.
        self.roll_action_bar = Gtk.ActionBar()
        roll_grid.attach_next_to(
            self.roll_action_bar,
            roll_scroll_win,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )

        # Create the template list buttons.
        roll_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(roll_btn_box.get_style_context(), 'linked')
        self.roll_action_bar.pack_start(roll_btn_box)
        self.edit_btn = Gtk.Button()
        self.edit_btn.add(load_symbolic('edit'))
        self.edit_btn.set_tooltip_text('Edit selected roll')
        self.delete_btn = Gtk.Button()
        self.delete_btn.add(load_symbolic('list-remove'))
        self.delete_btn.set_tooltip_text('Remove selected roll')
        roll_btn_box.add(self.edit_btn)
        roll_btn_box.add(self.delete_btn)

        # Create the roll drag and drop help text.
        drag_roll_lbl = Gtk.Label(
            'Drag and drop to rearrange roll order',
        )
        drag_roll_lbl.set_margin_top(10)
        roll_grid.attach_next_to(
            drag_roll_lbl,
            self.roll_action_bar,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )

        self.style_provider = Gtk.CssProvider()
        self.style_context = Gtk.StyleContext()
        self.style_context.add_provider_for_screen(
            Gdk.Screen.get_default(),
            self.style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
        self.style_provider.load_from_data(style_css)

        save_btn = self.get_widget_for_response(
            response_id=Gtk.ResponseType.OK,
        )
        save_btn.set_can_default(True)
        save_btn.grab_default()

        self.add_btn.connect(
            'clicked',
            lambda x: self.add_roll(),
        )
        self.edit_btn.connect(
            'clicked',
            lambda x: self.edit_roll(),
        )
        self.delete_btn.connect(
            'clicked',
            lambda x: self.remove_roll(),
        )
        self.crit_cbox.connect(
            'changed',
            lambda x: self.update_multipler_active(),
        )
        self.roll_tree.connect(
            'row-activated',
            lambda x, y, z: self.edit_roll(),
        )
        self.roll_tree.connect(
            'drag-end',
            lambda x, y: self.reorder_rolls(),
        )
        self.desc_ent.connect(
            'changed',
            lambda x: self.check_edit_name(),
        )

        self.register_limit_inputs()

        if self.name is not None:
            self.name_ent.set_text(self.name)
        self.update_list()

        self.show_all()

    def register_limit_inputs(self):
        number_inputs = [
            self.mod_ent, self.min_value_ent,
        ]
        count_inputs = [
            self.count_ent, self.die_ent, self.crit_ent,
        ]

        for input in number_inputs:
            input.connect('changed', NaturalOneWindow.limit_number_input)

        for input in count_inputs:
            input.connect(
                'changed',
                lambda i=input: NaturalOneWindow.limit_number_input(
                    i, allow_negative=False
                )
            )

    def check_edit_name(self):
        desc = self.desc_ent.get_text()
        for i in range(0, len(self.rolls)):
            if self.rolls[i]['description'] == desc:
                self.add_btn.set_label('Edit Roll')
                return

        self.add_btn.set_label('Add Roll')

    def update_list(self):
        self.roll_store.clear()
        for index, item in enumerate(self.rolls):
            mod_output = '{sign}{mod}'.format(
                sign=sign(item['mod']),
                mod=item['mod'],
            ) if item['mod'] else ''

            row = [
                index,
                item['description'],
                '{count}d{die}{mods}'.format(
                    count=item['count'],
                    die=item['die'],
                    mods=mod_output,
                ),
            ]
            if item['crit_option'] == CriticalOptions.MULTIPLY:
                row.append('Multiply x{crit_mod}'.format(crit_mod=item['crit_mod']))
            elif item['crit_option'] == CriticalOptions.MAXIMIZE:
                row.append('Maximize')
            elif item['crit_option'] == CriticalOptions.NO_CHANGE:
                row.append('No change')
            elif item['crit_option'] == CriticalOptions.ONLY:
                row.append('Only')
            else:
                row.append('N/A')
            self.roll_store.append(row)

    def update_multipler_active(self):
        iter = self.crit_cbox.get_active_iter()
        if iter is None:
            return
        on_crit_id = self.crit_cbox.get_model()[iter][1]
        self.crit_ent.set_sensitive(on_crit_id == CriticalOptions.MULTIPLY)

    def reorder_rolls(self):
        new_rolls = []
        for row_index in range(len(self.roll_store)):
            old_index = self.roll_store[row_index][0]
            new_rolls.append(self.rolls[old_index])
        self.rolls = new_rolls

    def check_roll_validity(self, roll):
        NaturalOneWindow.remove_error(self.count_ent)
        NaturalOneWindow.remove_error(self.die_ent)
        NaturalOneWindow.remove_error(self.mod_ent)
        NaturalOneWindow.remove_error(self.crit_ent)
        NaturalOneWindow.remove_error(self.min_value_ent)
        NaturalOneWindow.remove_error(self.desc_ent)

        valid = True

        try:
            assert roll['description'] != ''
        except AssertionError:
            NaturalOneWindow.add_error(self.desc_ent)
            NaturalOneWindow.show_popup(self.desc_error_popover)
            valid = False

        try:
            roll['count'] = int(roll['count'])
            assert roll['count'] >= 1
        except (ValueError, AssertionError):
            NaturalOneWindow.add_error(self.count_ent)
            NaturalOneWindow.show_popup(self.count_error_popover)
            valid = False

        try:
            roll['die'] = int(roll['die'])
            assert roll['die'] >= 1
        except (ValueError, AssertionError):
            NaturalOneWindow.add_error(self.die_ent)
            NaturalOneWindow.show_popup(self.die_error_popover)
            valid = False

        try:
            roll['mod'] = int(roll['mod'])
        except (ValueError, AssertionError):
            NaturalOneWindow.add_error(self.mod_ent)
            NaturalOneWindow.add_error(self.mod_error_popover)
            valid = False

        if roll['crit_option'] == CriticalOptions.MULTIPLY:
            try:
                roll['crit_mod'] = int(roll['crit_mod'])
                assert roll['crit_mod'] >= 1
            except (ValueError, AssertionError):
                NaturalOneWindow.add_error(self.crit_ent)
                NaturalOneWindow.show_popup(self.crit_error_popover)
                valid = False

        return valid

    def get_roll_data(self):
        count = self.count_ent.get_text().strip()
        die = self.die_ent.get_text().strip()
        mod = self.mod_ent.get_text().strip()
        mod_every = self.mod_chk.get_active()
        crit_mod = self.crit_ent.get_text().strip()
        min_value = self.min_value_ent.get_text().strip()
        desc = self.desc_ent.get_text().strip()

        iter = self.crit_cbox.get_active_iter()
        if iter is None:
            return
        crit_option = self.crit_cbox.get_model()[iter][1]

        roll = {
            'description': desc,
            'count': count,
            'die': die,
            'mod': mod,
            'mod_every': mod_every,
            'crit_option': crit_option,
            'crit_mod': crit_mod,
            'min_value': min_value
        }

        valid = self.check_roll_validity(roll)

        return roll, valid

    def add_roll(self):
        roll, valid = self.get_roll_data()
        if not valid:
            return

        add_as_new = True
        for i in range(0, len(self.rolls)):
            if self.rolls[i]['description'] == roll['description']:
                self.rolls[i] = roll
                add_as_new = False
        if add_as_new:
            self.rolls.append(roll)

        self.check_edit_name()

        self.update_list()

    def edit_roll(self):
        index = NaturalOneWindow.get_selected_index(self.roll_tree)
        if index is None:
            return

        roll = self.rolls[index]
        self.count_ent.set_text(str(roll['count']))
        self.die_ent.set_text(str(roll['die']))
        self.mod_ent.set_text(str(roll['mod']))
        self.mod_chk.set_active(roll['mod_every'])
        if roll['crit_option'] == CriticalOptions.MULTIPLY:
            self.crit_ent.set_sensitive(True)
            self.crit_ent.set_text(str(roll['crit_mod']))
        else:
            self.crit_ent.set_sensitive(False)
            self.crit_ent.set_text("")
        self.crit_cbox.set_active(roll['crit_option'])
        self.min_value_ent.set_text(str(roll['min_value']))
        self.desc_ent.set_text(roll['description'])

        self.check_edit_name()

    def remove_roll(self):
        indices = NaturalOneWindow.get_selected_indices(self.roll_tree)
        if not indices:
            return

        message_text = 'Are you sure you want to remove ' \
            '{plural_adj} {count} roll{plural}?'.format(
                plural_adj=pluralize_adj(indices),
                count=len(indices),
                plural=pluralize(indices),
            )
        if not show_question(self, 'Templates', message_text):
            return

        for index in reversed(indices):
            del self.rolls[index]

        self.update_list()
