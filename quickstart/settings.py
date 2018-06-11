import json
from quickstart.prompt import select, print_option, prompt, print_settings


def load_settings(file):
    with open(file, 'r') as load:
        return json.load(load)
    return {}


def parse_type(type):
    if type == 'bool':
        return bool
    elif type == 'str':
        return str
    elif type == 'int':
        return int
    elif type == 'float':
        return float


def is_sub_group(group):
    for key in group:
        if key not in ('help', 'default', 'type', 'choices'):
            return True


def prompt_users(options, sub=""):
    result = {}
    for key, value in options.items():
        help = str()
        default = None
        type = str
        choices = None
        if isinstance(value, str):
            help = value
            result[sub + key] = [
                help,
                prompt(
                    sub + key,
                    help=help,
                    default=default,
                    tp=type,
                    choices=choices)
            ]
        elif isinstance(value, list):
            help = value[0]
            if len(value) >= 2:
                if isinstance(value[1], list):
                    choices = value[1]
                else:
                    default = value[1]
            if len(value) >= 3:
                if isinstance(value[2], list):
                    choices = value[2]
                else:
                    type = parse_type(value[2])
            result[sub + key] = [
                help,
                prompt(
                    sub + key,
                    help=help,
                    default=default,
                    tp=type,
                    choices=choices)
            ]
        elif isinstance(value, dict):
            if "help" in value:
                help = value['help']
            if 'default' in value:
                default = value['default']
            if is_sub_group(value):
                print("\033[1;97m{:^{}}\033[0m".format(sub + key, 40))
                print("=" * 40)
                type = bool
                if "help" in value:
                    help = value['help']
                if "force" not in value or value['force'] is False:
                    result[sub + key] = [
                        help,
                        prompt(
                            sub + key,
                            help=help,
                            default=default,
                            tp=type,
                            choices=choices)
                    ]
                if (sub + key in result and result[sub + key][1] is True) or (
                        'force' in value and value['force'] is True):
                    if "help" in value:
                        del value["help"]
                    if "default" in value:
                        del value["default"]
                    if "force" in value:
                        del value["force"]
                    result = {**result, **prompt_users(value, key + '.')}

            else:
                if 'type' in value:
                    type = parse_type(value['type'])
                if 'choices' in value:
                    choices = value['choices']
                result[sub + key] = [
                    help,
                    prompt(
                        sub + key,
                        help=help,
                        default=default,
                        tp=type,
                        choices=choices)
                ]
    return result


def get_options(file):
    return prompt_users(load_settings(file))
