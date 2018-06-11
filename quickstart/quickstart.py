from quickstart.prompt import select, print_option, prompt, print_settings
from quickstart.settings import get_options


def main():
    language = select(["C", "C++", "Python", "VimL"])
    file = {
        "C": "c.json",
        "C++": "cpp.json",
        "Python": "python.json",
        "VimL": "vimscript.json"
    }
    options = get_options("./options/{}".format(file[language]))
    print("=" * 40)
    print("{:^{}}".format("Verify Settings", 40))
    print("=" * 40)
    print_settings(options)
