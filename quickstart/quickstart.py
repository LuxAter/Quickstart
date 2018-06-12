import sys
import os
from quickstart.prompt import select, print_option, prompt, print_settings
from quickstart.settings import get_options
from quickstart.generator import generate


def main():
    defaults=False
    dry = False
    if '--default' in sys.argv:
        defaults=True
    if '--dry' in sys.argv:
        dry = True
    language = select(["C", "C++", "Python", "VimL"])
    file = {"C": "c", "C++": "cpp", "Python": "python", "VimL": "vimscript"}
    options = get_options(os.path.dirname(__file__) + "/options/{}.json".format(file[language]), defaults)
    print("=" * 40)
    print("{:^{}}".format("Verify Settings", 40))
    print("=" * 40)
    print_settings(options)
    generate("{}".format(file[language]),
             os.path.dirname(__file__) + "/options/{}.json".format(file[language]), options, dry)
