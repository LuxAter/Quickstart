from entry import options, actions


def main():
    opts = options("cpp", "C++")
    opts.add_entry("Name", "Project name", type=str)
    opts.add_entry("Description", "Project description", type=str)
    opts.group("Directories")
    opts.add_entry("Root", "Root directory", default=".")
    opts.add_entry("Source", "Source directory", default="source")
    opts.add_entry("Include", "Include directory", default="include")
    opts.add_entry("Build", "Build directory", default="build")
    opts.add_entry("External", "External directory", default="external")
    opts.group("Git")
    opts.add_entry("Repo", "Create a repository for the project",
                   action=actions.EXE, type=bool, default=True, ext="git init .")
    opts.add_entry("Ignore", "Create default git ignore file", action=actions.FILE,
                   type=bool, default=True, require="Repo", ext=".gitignore")
    opts.add_entry("Remote", "Remote url for git repository", action=actions.EXE,
                   type=str, require="Repo", ext="git remote add origin {{Remote}}")
    opts.group("UnitTests")
    opts.add_entry("UnitTests", "Enable unit testing using Gtest", action=actions.FILE,
                   type=bool, default=True, ext=[("test/Makefile", "{{Test}}/Makefile"), ("external/Makefile", "{{External}}/Makefile")])
    opts.add_entry("Test", "Test directory", default="test")
    opts.add_entry("GTest", "Add google test as a submodule", type=bool, default=True, require="UnitTests",
                   ext="git submodule add https://github.com/google/googletest {{External}}")
    opts.group("Documentation")
    opts.add_entry("Doc", "Add documentation to the project",
                   type=bool, default=True)
    opts.add_entry("DocDir", "Documentation directory", default="docs")
    opts.add_entry("DocSys", "Documentation engine", type=str, default="None", choices={
                   "None", "Sphinx", "MkDocs", "Doxygen"}, require="Doc")
    opts.add_entry("Author", "Sphinx author", type=str,
                   require=("DocSys", "Sphinx"))
    opts.add_entry("Copyright", "Sphinx copyright",
                   type=str, require=("DocSys", "Sphinx"))
    opts.prompt()
    print(opts.get_data())
    opts.run()


if __name__ == "__main__":
    main()
