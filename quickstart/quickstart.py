from entry import options, actions


def main():
    opts = options()
    opts.add_entry("Name", "Project name", type=str)
    opts.add_entry("Description", "Project description", type=str)
    opts.group("Directories")
    opts.add_entry("Root", "Root directory")
    opts.add_entry("Source", "Source directory")
    opts.add_entry("Include", "Include directory")
    opts.add_entry("Build", "Build directory")
    opts.add_entry("External", "External directory")
    opts.group("Git")
    opts.add_entry("Repo", "Create a repository for the project",
                   action=actions.EXE, type=bool, default=True, ext="git init .")
    opts.add_entry("Ignore", "Create default git ignore file", action=actions.FILE,
                   type=bool, default=True, require="Repo", ext=".gitignore")
    opts.add_entry("Remote", "Remote url for git repository",
                   type=str, require="Repo")
    opts.group("UnitTests")
    opts.add_entry("UnitTests", "Enable unit testing using Gtest",
                   type=bool, default=True, ext=["test/Makefile", "external/Makefile"])
    opts.add_entry("GTest", "Add google test as a submodule", type=bool, default=True, require="UnitTests",
                   ext="git submodule add https://github.com/google/googletest {{External}}")
    opts.prompt()
    print(opts.get_data())
    opts.run()


if __name__ == "__main__":
    main()
