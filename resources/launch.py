# -*- coding: utf-8 -*-
import json
import os
import sys

import resources.io as io


def get_menu_data():
    try:
        with open('resources/ui/menu.xml', 'r') as menu_file:
            return menu_file.read()
    except IOError as e:
        print('get_menu_data(): Error reading menu data:\n{error}'.format(
            error=e,
        ))
        sys.exit()


def get_style_data():
    try:
        with open('resources/ui/style.css', 'r') as style_file:
            return style_file.read()
    except IOError as e:
        print('get_style_data():  Error reading style data:\n{error}'.format(
            error=e,
        ))
        sys.exit()


def get_weapon_data(systems):
    system_names = [
        system['name'] for system in systems['systems']
        if system['enabled']
    ]
    data = []
    for system in systems['systems']:
        if not system['enabled']:
            continue
        if system['user_added']:
            path = os.path.join(io.get_systems_dir(), system['filename'])
        else:
            path = os.path.join('resources/data/weapons', system['filename'])
        try:
            with open(path) as data_file:
                data.append(json.load(data_file))
        except (IOError, TypeError, ValueError) as e:
            print('get_weapon_data(): Error reading weapons data file '
                  '{path}:\n{error}'.format(
                      path=path,
                      error=e,
                  ),
                  )
            sys.exit()

    return system_names, data
