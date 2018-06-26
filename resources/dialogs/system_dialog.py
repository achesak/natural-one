# -*- coding: utf-8 -*-
import copy
import json
import os

from gi.repository import Gtk

from resources.dialogs.generic_dialogs import (
    show_error,
    show_message,
    show_question,
)
import resources.io as io
from resources.load_images import load_symbolic
from resources.utility import pluralize, pluralize_adj
from resources.window import NaturalOneWindow


class SystemDialog(Gtk.Dialog):

    def __init__(self, parent, systems, system_names, weapon_data):

        self.systems = copy.deepcopy(systems['systems'])
        self.system_names = copy.deepcopy(system_names)
        self.weapon_data = copy.deepcopy(weapon_data)

        Gtk.Dialog.__init__(
            self,
            'Systems',
            parent,
            Gtk.DialogFlags.MODAL,
            use_header_bar=True,
        )
        self.set_size_request(500, 650)
        self.add_button('Cancel', Gtk.ResponseType.CANCEL)
        self.add_button('OK', Gtk.ResponseType.OK)

        # Create the header bar.
        header = self.get_header_bar()
        header.set_title('Systems')

        # Create the systems grid.
        system_grid = Gtk.Grid()
        system_grid.set_row_spacing(5)
        system_grid.set_column_spacing(12)
        system_grid.set_border_width(18)
        self.get_content_area().add(system_grid)

        # Create the systems main label.
        system_lbl = Gtk.Label()
        system_lbl.set_markup('<span size="x-large">Manage Systems</span>')
        system_lbl.set_alignment(0, 0.5)
        system_lbl.set_margin_bottom(10)
        system_grid.add(system_lbl)

        # Create the systems list.
        system_scroll_win = Gtk.ScrolledWindow()
        system_scroll_win.set_hexpand(True)
        system_scroll_win.set_vexpand(True)
        system_grid.attach_next_to(
            system_scroll_win,
            system_lbl,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )
        self.system_store = Gtk.ListStore(bool, str, str)
        self.system_tree = Gtk.TreeView(model=self.system_store)
        self.system_tree.set_reorderable(True)
        self.system_tree.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        enable_text = Gtk.CellRendererToggle()
        enable_text.connect(
            'toggled',
            lambda widget, path: self.toggle_system_enabled(path),
        )
        self.enable_col = Gtk.TreeViewColumn('Enabled', enable_text, active=0)
        self.system_tree.append_column(self.enable_col)
        roll_text = Gtk.CellRendererText()
        self.system_col = Gtk.TreeViewColumn('System', roll_text, text=1)
        self.system_col.set_expand(True)
        self.system_tree.append_column(self.system_col)
        source_text = Gtk.CellRendererText()
        self.source_col = Gtk.TreeViewColumn('Source', source_text, text=2)
        self.system_tree.append_column(self.source_col)
        system_scroll_win.add(self.system_tree)

        # Create the system list action bar.
        self.system_action_bar = Gtk.ActionBar()
        system_grid.attach_next_to(
            self.system_action_bar,
            system_scroll_win,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )

        # Create the system list buttons.
        system_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(
            system_btn_box.get_style_context(),
            'linked',
        )
        self.system_action_bar.pack_start(system_btn_box)
        self.add_btn = Gtk.Button()
        self.add_btn.add(load_symbolic('list-add'))
        self.add_btn.set_tooltip_text('Add system')
        system_btn_box.add(self.add_btn)
        self.delete_btn = Gtk.Button()
        self.delete_btn.add(load_symbolic('list-remove'))
        self.delete_btn.set_tooltip_text('Remove selected systems')
        system_btn_box.add(self.delete_btn)
        self.select_all_btn = Gtk.Button()
        self.select_all_btn.add(load_symbolic('edit-select-all'))
        self.select_all_btn.set_tooltip_text('Toggle enable/disable all')
        self.system_action_bar.pack_end(self.select_all_btn)

        # Create the systems drag and drop help text.
        drag_sys_lbl = Gtk.Label('Drag and drop to rearrange systems')
        drag_sys_lbl.set_margin_top(10)
        system_grid.attach_next_to(
            drag_sys_lbl,
            self.system_action_bar,
            Gtk.PositionType.BOTTOM,
            1, 1,
        )

        self.update_systems_list()

        self.system_tree.connect(
            'drag-end',
            lambda x, y: self.reorder_systems(),
        )
        self.add_btn.connect(
            'clicked',
            lambda x: self.add_system(),
        )
        self.delete_btn.connect(
            'clicked',
            lambda x: self.remove_system(),
        )
        self.select_all_btn.connect(
            'clicked',
            lambda x: self.toggle_all_enable_state(),
        )

        save_btn = self.get_widget_for_response(
            response_id=Gtk.ResponseType.OK
        )
        save_btn.set_can_default(True)
        save_btn.grab_default()

        self.show_all()

    def update_systems_list(self):
        self.system_store.clear()
        for system in self.systems:
            source = 'User' if system['user_added'] else 'Base'
            self.system_store.append(
                [system['enabled'], system['name'], source]
            )

    def toggle_system_enabled(self, path):
        self.system_store[path][0] = not self.system_store[path][0]
        self.systems[int(path)]['enabled'] ^= 1

    def toggle_all_enable_state(self):
        state = False
        for row_index in range(len(self.system_store)):
            if not self.system_store[row_index][0]:
                state = True
                break

        for row_index in range(len(self.system_store)):
            self.system_store[row_index][0] = state
            self.systems[row_index]['enabled'] = state

    def reorder_systems(self):
        new_systems = []
        for row_index in range(len(self.system_store)):
            system_name = self.system_store[row_index][1]
            original_index = -1
            for system_index in range(len(self.systems)):
                if self.systems[system_index]['name'] == system_name:
                    original_index = system_index
                    break
            new_systems.append(copy.deepcopy(self.systems[original_index]))

        self.systems = new_systems

    def add_system(self):
        dialog = Gtk.FileChooserDialog(
            'Add System',
            self,
            Gtk.FileChooserAction.OPEN,
            (
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK, Gtk.ResponseType.OK,
            ),
        )
        dialog.set_current_folder(os.path.expanduser('~'))

        filter_json = Gtk.FileFilter()
        filter_json.set_name('JSON system files')
        filter_json.add_mime_type('application/json')
        dialog.add_filter(filter_json)

        filter_any = Gtk.FileFilter()
        filter_any.set_name('Any files')
        filter_any.add_pattern('*')
        dialog.add_filter(filter_any)

        response = dialog.run()
        filename = dialog.get_filename()
        dialog.destroy()

        if response != Gtk.ResponseType.OK or not filename:
            return

        errors = []
        system = None
        system_name = None

        try:
            with open(filename) as system_file:
                system = json.load(system_file)
        except (IOError, TypeError, ValueError):
            errors.append(
                'File has significant issues. Is it in the correct format?'
            )

        if system is not None:
            try:
                system_name = system['name']
            except (TypeError, ValueError):
                errors.append('System name is missing.')

        if system_name in self.system_names:
            errors.append('System name is already in use.')

        if errors:
            show_error(
                self,
                'Systems',
                'There was at least one issue with the selected file:\n\n'
                '\n'.join(errors),
            )
            return

        new_filename = io.add_system(filename)

        self.systems.append({
            'name': system_name,
            'filename': new_filename,
            'enabled': True,
            'user_added': True
        })
        self.system_names.append(system_name)

        self.update_systems_list()

    def remove_system(self):
        indices = NaturalOneWindow.get_selected_indices(self.system_tree)
        if not indices:
            return

        message_text = 'Are you sure you want to remove ' \
            '{plural_adj} {count} system{plural}'.format(
                plural_adj=pluralize_adj(indices),
                count=len(indices),
                plural=pluralize(indices),
            )
        if not show_question(self, 'Systems', message_text):
            return

        show_base_message = False
        for index in indices:
            if not self.systems[index]['user_added']:
                show_base_message = True
                continue
            io.remove_system(self.systems[index]['filename'])
            name_index = self.system_names.index(self.systems[index]['name'])
            del self.system_names[name_index]
            del self.systems[index]

        self.update_systems_list()

        if show_base_message:
            show_message(
                self,
                'Systems',
                'Systems built in to Natural One cannot be removed.',
            )
