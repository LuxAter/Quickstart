from quickstart.getch import getch

def print_option(name, help, option, len_name=0, len_help=0):
    print("\033[96m{:{}}\033[95m[{:{}}]\033[0;1m: {}\033[0m".format(name, len_name, help, len_help, option))

def prompt(name, help, default=None, tp=str, choices=None):
    while True:
        string = "\033[96m{}\033[95m[{}]".format(name, help)
        if default is not None:
            string += "\033[92m<{}>".format(default)
        if choices is not None:
            string += "\033[94m{{{}}}".format(choices)
        string += "\033[0m: "
        res = input(string)
        if res == str() and default is not None:
            return default
        if tp == bool:
            if res.lower() in ('t', 'true', 'yes', 'y'):
                return True
            elif res.lower() in ('f', 'false', 'no', 'n'):
                return False
        else:
            try:
                ret = tp(res)
                if choices is not None and ret in choices:
                    return ret
                elif choices is None:
                    return ret
            except:
                pass

def select(choices):
    selected = 0
    while True:
        for i, opt in enumerate(choices):
            if i == selected:
                print("{:{}}: \033[7m{}\033[0m".format(i, len(str(len(choices))), opt))
            else:
                print("{:{}}: {}".format(i, len(str(len(choices))), opt))
        print("\033[2K", end='')
        ch = input('>> ')
        if ch == "":
            return choices[selected]
        elif ch.isdigit() and int(ch) < len(choices) and int(ch) >= 0:
            selected = int(ch)
        else:
            if ch in choices:
                selected = choices.index(ch)
        print("\033[{}F".format(len(choices) + 1), end='')

def print_settings(settings):
    len_name = 0
    len_help = 0
    for key, value in settings.items():
        len_name = max(len_name, len(key))
        len_help = max(len_help, len(value[0]))
    for key, setting in settings.items():
        print_option(key, setting[0], setting[1], len_name, len_help)
