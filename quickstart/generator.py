import re
import os
import subprocess
from jinja2 import Environment, PackageLoader, select_autoescape
from quickstart.settings import load_settings


def replace_string(options, string):
    pattern = re.compile(r'{{(' + "|".join(options.keys()) + ')}}')
    result = pattern.sub(lambda x: options[x.group(1)][1], string)
    name = re.compile(r'{{(Name)}}')
    result = name.sub(lambda x: options['Name'][1], result)
    return result


def valid_event(event, options, type):
    if type == "DIR":
        if len(event) == 1:
            return True
        elif len(event) == 2 and event[0] in options and options[event[0]][1]:
            return True
        elif len(
                event
        ) == 3 and event[0] in options and options[event[0]][1] == event[1]:
            return True
    elif type == "FILE":
        if len(event) == 2:
            return True
        elif len(event) == 3 and isinstance(event[0], list):
            state = True
            for cond in event[0]:
                if isinstance(cond, list) and (cond[0] not in options or
                                               options[cond[0]][1] != cond[1]):
                    state = False
                elif not isinstance(cond, list) and (cond not in options
                                                     or not options[cond][1]):
                    state = False
            return state
        elif len(event) == 3 and event[0] in options and options[event[0]][1]:
            return True
        elif len(
                event
        ) == 4 and event[0] in options and options[event[0]][1] == event[1]:
            return True
    elif type == "CMD":
        if len(event) == 1:
            return True
        elif len(event) == 2 and isinstance(event[0], list):
            state = True
            for cond in event[0]:
                if isinstance(cond, list) and (cond[0] not in options or
                                               options[cond[0]][1] != cond[1]):
                    state = False
                elif cond not in options or not options[cond][1]:
                    state = False
            return state
        elif len(event) == 2 and event[0] in options and options[event[0]][1]:
            return True
        elif len(
                event
        ) == 3 and event[0] in options and options[event[0]][1] == event[1]:
            return True
    return False

def set_value(dic, key, value):
    if isinstance(key, str):
        set_value(dic, key.split('.'), value)
    elif isinstance(key, list):
        print(key)
        if len(key) != 1:
            if key[0] not in dic:
                dic[key[0]] = dict()
            else:
                if not isinstance(dic[key[0]], dict):
                    dic[key[0]] = {key[0]: dic[key[0]]}
            print(key[0])
            set_value(dic[key[0]], key[1:], value)
        else:
            print(dic)
            dic[key[0]] = value

def generate_cmds(cmds, options, env, dry):
    for event in cmds:
        if valid_event(event, options, "CMD"):
            print("EXECUTE:", replace_string(options, event[-1]))
            if not dry:
                cmd = replace_string(options, event[-1]).split()
                print(cmd)
                dir = None
                if cmd[0] == 'cd' and cmd[2] == '&&':
                    dir = cmd[1]
                    cmd = cmd[3:]
                print(cmd, dir)
                if dir is not None:
                    subprocess.Popen(cmd, cwd=dir)
                else:
                    subprocess.Popen(cmd)


def generate_files(files, options, env, dry):
    generator_variables = {}
    for key, value in options.items():
        print(key, value)
        set_value(generator_variables, key, value[-1])
    for event in files:
        if valid_event(event, options, "FILE"):
            template = env.get_template(event[-1])
            print("GEN FILE:", replace_string(options, event[-2]), event[-1])
            if not dry:
                with open(replace_string(options, event[-2]), 'w') as file:
                    file.write(template.render(**generator_variables))


def generate_dirs(dirs, options, env, dry):
    for event in dirs:
        if valid_event(event, options, "DIR"):
            print("GEN DIR:", replace_string(options, event[-1]))
            if not dry and not os.path.exists(replace_string(options, event[-1])):
                os.mkdir(replace_string(options, event[-1]))


def generate(language, file, options, dry):
    env = Environment(
        loader=PackageLoader('quickstart', 'templates/{}'.format(language)),
        autoescape=select_autoescape(['html', 'xml']))
    print(env.list_templates())
    events = load_settings(file)['Events']
    if 'Directories' in events:
        generate_dirs(events['Directories'], options, env, dry)
    if 'Files' in events:
        generate_files(events['Files'], options, env, dry)
    if 'Cmds' in events:
        generate_cmds(events['Cmds'], options, env, dry)
