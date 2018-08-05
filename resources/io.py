# -*- coding: utf-8 -*-
import json
import os
import platform
import shutil
import sys
import uuid


def get_main_dir():
    # Windows support here for future full implementation.
    if platform.system().lower() == 'windows':
        path = os.path.join(os.environ['LOCALAPPDATA'], '\\naturalone')
    else:
        path = os.path.join(os.path.expanduser('~'), '.local/share/naturalone')

    if not os.path.exists(path):
        os.makedirs(path)

    return path


def get_systems_dir():
    root_path = get_main_dir()
    systems_path = os.path.join(root_path, 'systems')

    if not os.path.exists(systems_path):
        os.makedirs(systems_path)

    return systems_path


def get_systems_settings_path():
    root_path = get_main_dir()
    return os.path.join(root_path, 'systems.json')


def create_systems_settings():
    try:
        shutil.copyfile(
            'resources/data/weapons.json',
            get_systems_settings_path(),
        )
    except IOError:
        print('IOError copying systems settings')
        sys.exit()


def load_systems_settings():
    path = get_systems_settings_path()
    if not os.path.exists(path):
        create_systems_settings()
    with open(path, 'r') as systems_file:
        try:
            return json.load(systems_file)
        except (IOError, TypeError, ValueError):
            create_systems_settings()
            return load_systems_settings()


def load_default_systems_settings():
    with open('resources/data/weapons.json', 'r') as systems_file:
        try:
            return json.load(systems_file)
        except (IOError, TypeError, ValueError):
            return {"systems": []}


def save_systems_settings(systems):
    try:
        with open(get_systems_settings_path(), 'w') as systems_file:
            json.dump(systems, systems_file)
    except IOError:
        print('IOError saving systems')


def get_template_path():
    root_path = get_main_dir()
    return os.path.join(root_path, 'templates.json')


def load_templates():
    with open(get_template_path(), 'a+') as template_file:
        template_file.seek(0)
        try:
            return json.load(template_file)
        except (IOError, TypeError, ValueError):
            template_file.write('[]')
            return []


def save_templates(templates):
    write_templates(get_template_path(), templates)


def read_templates(filename):
    with open(filename, 'r') as template_file:
        try:
            return json.load(template_file)
        except (IOError, TypeError, ValueError):
            print('Error reading templates')


def write_templates(filename, templates):
    try:
        with open(filename, 'w') as template_file:
            json.dump(templates, template_file)
    except IOError:
        print('IOError writing templates')


def add_system(filename):
    new_filename = '{new_filename}.json'.format(
        new_filename=str(uuid.uuid4()),
    )
    shutil.copyfile(
        filename,
        os.path.join(get_systems_dir(), new_filename),
    )
    return new_filename


def remove_system(filename):
    system_path = os.path.join(
        get_systems_dir(),
        filename,
    )
    if os.path.exists(system_path):
        os.remove(system_path)
