
import re
import os
from enum import Enum


class actions(Enum):
    EXE = 0,
    DIR = 1,
    FILE = 2


class entry_data:
    def __init__(self, name_str, help_str=str(), action=None, type_=None, choices=list(), default=None, require=None, ext=None, lang=None):
        self.name = name_str
        self.help = help_str
        self.choices = choices
        self.type = type_
        self.default = default
        self.action = action
        self.require = require
        self.action_data = ext
        self.lang = lang
        self.value = None

    def check_int(self, string):
        try:
            int(string)
        except ValueError:
            return False
        return True

    def check_float(self, string):
        try:
            float(string)
        except ValueError:
            return False
        return True

    def gen_folder(self, dest):
        if dest == str():
            return
        if os.path.exists(os.path.dirname(dest)) is False:
            self.gen_folder(os.path.dirname(dest))
        os.mkdir(dest)

    def write_file(self, source, dest, data):
        source = os.path.join(os.path.dirname(__file__),
                              "templates/", self.lang, source)
        if os.path.isfile(source) is False:
            print(source)
            return False
        with open(source, 'r') as file:
            filedata = file.read()
        pattern = re.compile('|'.join(data.keys()))
        filedata = pattern.sub(
            lambda x: data[x.group()], filedata)
        with open(dest, 'w') as file:
            file.write(filedata)
        return True

    def create_file(self, dest):
        return True

    def display(self, color=True):
        string = str()
        if self.name:
            if color:
                string += "\033[1;97m"
            string += self.name
            if color:
                string += "\033[0m"
            string += ': '
        if self.help:
            if color:
                string += "\033[36m"
            string += self.help
            if color:
                string += "\033[0m"
        if self.default:
            if color:
                string += "\033[35m"
            string += ' [{}]'.format(self.default)
            if color:
                string += "\033[0m"
        if self.choices:
            if color:
                string += "\033[34m"
            string += ' {}'.format(self.choices)
            if color:
                string += "\033[0m"
        if color:
            string += "\033[1m"
        string += ' >> '
        if color:
            string += "\033[0m"
        if self.value:
            string += self.value
        return string

    def prompt(self, color=True):
        if self.value:
            print(self.display(color))
            return
        while self.value is None:
            self.value = input(self.display(color))
            if self.value == str() and self.default:
                self.value = self.default
                return
            if self.check_int(self.value) and self.type == int:
                self.value = int(self.value)
            elif self.check_float(self.value) and self.type == float:
                self.value = float(self.value)
            elif self.type == bool:
                if self.value.lower() in ('true', '1', 'y', 't', 'yes'):
                    self.value = True
                elif self.value.lower() in ('false', '0', 'n', 'f', 'no'):
                    self.value = False
            elif self.type == str or self.type == None:
                self.value = str(self.value)
            elif self.type not in (int, float, bool, str, None) and callable(self.type):
                self.value = self.type(self.value)
            else:
                self.value = None
            if self.value is None:
                print("{:{}}Invalid Type".format("", len(self.name) + 2))
                continue
            if self.choices and self.value not in self.choices:
                print("{:{}}Choice not in choices".format(
                    "", len(self.name) + 2))
                self.value = None

    def run_action(self, data):
        if self.action_data is None or self.action is None or self.value is False or self.value is None:
            return
        pattern = re.compile('|'.join(data.keys()))
        if self.action_data and isinstance(self.action_data, str):
            self.action_data = pattern.sub(
                lambda x: data[x.group()], self.action_data)
        elif isinstance(self.action_data, tuple):
            self.action_data = tuple([pattern.sub(
                lambda x: data[x.group()], prt) for prt in self.action_data])
        elif isinstance(self.action_data, list):
            for i, cmd in enumerate(self.action_data):
                if isinstance(cmd, tuple):
                    cmd = tuple([pattern.sub(
                        lambda x: data[x.group()], prt) for prt in cmd])
                else:
                    cmd = pattern.sub(
                        lambda x: data[x.group()], cmd)
                self.action_data[i] = cmd
        if self.action is actions.EXE:
            if isinstance(self.action_data, list) or isinstance(self.action_data, tuple):
                for exe in self.action_data:
                    os.system(exe)
            else:
                os.system(self.action_data)
        elif self.action is actions.DIR:
            if isinstance(self.action_data, list) or isinstance(self.action_data, tuple):
                for folder in self.action_data:
                    self.gen_folder(folder)
            else:
                self.gen_folder(self.action_data)
        elif self.action is actions.FILE:
            if isinstance(self.action_data, list):
                for filecmd in self.action_data:
                    if isinstance(filecmd, tuple):
                        source, dest = filecmd
                        if os.path.exists(os.path.dirname(dest)) is False:
                            self.gen_folder(os.path.dirname(dest))
                        if self.write_file(source, dest, data) is False:
                            print("Source file does not exist!")
                    else:
                        self.create_file(filecmd)
            elif isinstance(self.action_data, tuple):
                source, dest = self.action_data
                if os.path.exists(os.path.dirname(dest)) is False:
                    self.gen_folder(os.path.dirname(dest))
                if self.write_file(source, dest, data) is False:
                    print("Source file does not exist!")
            else:
                self.create_file(self.action_data)


class options:
    def __init__(self, lang, disp_lang=None):
        self.entries = {"null": []}
        self.current_group = "null"
        self.cmds = list()
        self.files = list()
        self.dirs = list()
        self.lang = lang
        self.disp_lang = disp_lang if disp_lang else lang

    def group(self, string):
        self.entries[string] = list()
        self.current_group = string

    def add_entry(self, name_str, help_str=str(), action=None, type=None, choices=list(), default=None, require=None, ext=None):
        self.entries[self.current_group].append(entry_data(
            name_str, help_str, action, type, choices, default, require, ext, self.lang))

    def prompt(self, color=True):
        data = dict()
        if color:
            print("\033[1;4;34m{:^40}\033[0m".format(self.disp_lang.title()))
        else:
            print("{:^40}".format(self.disp_lang.title()))
        for key, value in self.entries.items():
            if key != "null":
                if color:
                    print("\033[4;93m{:^40}\033[0m".format(key))
                else:
                    print("{:^40}".format(key))
            for entry in value:
                if entry.require is None:
                    entry.prompt(color)
                elif isinstance(entry.require, str) and entry.require in data and data[entry.require]:
                    entry.prompt(color)
                elif isinstance(entry.require, tuple) and entry.require[0] in data and data[entry.require[0]] == entry.require[1]:
                    entry.prompt(color)
                data[entry.name] = entry.value

    def get_data(self):
        data = dict()
        for key, value in self.entries.items():
            for entry in value:
                data[entry.name] = entry.value
        return data

    def run(self):
        data = dict()
        for key, value in self.get_data().items():
            data["{{" + key + "}}"] = value
        for key, value in self.entries.items():
            for entry in value:
                entry.run_action(data)
