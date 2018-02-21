
import re
from enum import Enum


class actions(Enum):
    EXE = 0,
    DIR = 1,
    FILE = 2


class entry_data:
    def __init__(self, name_str, help_str=str(), action=None, type_=None, choices=list(), default=None, require=None, ext=None):
        self.name = name_str
        self.help = help_str
        self.choices = choices
        self.type = type_
        self.default = default
        self.action = action
        self.require = require
        self.action_data = ext
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
        if self.action_data and isinstance(self.action_data, str):
            pattern = re.compile('|'.join(data.keys()))
            self.action_data = pattern.sub(
                lambda x: data[x.group()], self.action_data)
        elif isinstance(self.action_data, list):
            pattern = re.compile('|'.join(data.keys()))
            for cmd in self.action_data:
                cmd = pattern.sub(
                    lambda x: data[x.group()], cmd)
        print(self.action_data)
        if self.action is None:
            return
        if self.action is actions.EXE:
            return


class options:
    def __init__(self):
        self.entries = {"null": []}
        self.current_group = "null"
        self.cmds = list()
        self.files = list()
        self.dirs = list()

    def group(self, string):
        self.entries[string] = list()
        self.current_group = string

    def add_entry(self, name_str, help_str=str(), action=None, type=None, choices=list(), default=None, require=None, ext=None):
        self.entries[self.current_group].append(entry_data(
            name_str, help_str, action, type, choices, default, require, ext))

    def prompt(self, color=True):
        data = dict()
        for key, value in self.entries.items():
            if key != "null":
                if color:
                    print("\033[4;93m{:^40}\033[0m".format(key))
                else:
                    print("{:^40}".format(key))
            for entry in value:
                if entry.require is None or (entry.require in data and data[entry.require]):
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