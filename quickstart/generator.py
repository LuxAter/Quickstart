import quickstart.entry


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()


class generator():
    def __init__(self):
        self.title = "Quickstart Project Generator"
        self.languages = list()

    def select_lang(self, color=True):
        if color:
            print("\033[1;97m{:^40}\033[0m".format(self.title))
            print("\033[1;97m" + ('=' * 40) + "\033[0m")
        else:
            print("{:^40}".format(self.title))
            print('=' * 40)
        key = None
        selected = 0
        update = True
        while key != 13 and key != 3 and key != 113:
            if update is True:
                update = False
                for i, lang in enumerate(self.languages):
                    string = "[{:{}}] ".format(
                        i, len(str(len(self.languages))))
                    if i == selected:
                        if color:
                            string += "\033[7m"
                        else:
                            string += ">"
                    string += lang.disp_lang
                    if i == selected:
                        if color:
                            string += "\033[0m"
                        else:
                            string += "<"
                    print(string)
            key = ord(getch())
            if key == 66 and selected < len(self.languages) - 1:
                selected += 1
                update = True
                print("\033[{}A".format(len(self.languages) + 1))
            elif key == 65 and selected > 0:
                selected -= 1
                update = True
                print("\033[{}A".format(len(self.languages) + 1))
        if key == 3 or key == 113:
            return None
        else:
            return self.languages[selected]

    def run(self, color=True):
        self.languages = sorted(self.languages, key=lambda x: x.disp_lang)
        lang = self.select_lang(color)
        if lang:
            lang.prompt()
            lang.run()
        else:
            if color:
                print("\033[31mAbborting\033[0m")


GEN = generator()
