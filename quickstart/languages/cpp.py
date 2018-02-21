"""
Implements C++ Generator
"""

from generator import GEN
from entry import options, actions

OPTS = options("cpp", "C++")
OPTS.add_entry("Name", "Project name", type=str)
OPTS.add_entry("Description", "Project description", type=str)
OPTS.group("Directories")
OPTS.add_entry("Root", "Root directory", default=".")
OPTS.add_entry("Source", "Source directory", default="source")
OPTS.add_entry("Include", "Include directory", default="include")
OPTS.add_entry("Build", "Build directory", default="build")
OPTS.add_entry("External", "External directory", default="external")
OPTS.group("Git")
OPTS.add_entry("Repo", "Create a repository for the project",
               action=actions.EXE, type=bool, default=True, ext="git init .")
OPTS.add_entry("Ignore", "Create default git ignore file", action=actions.FILE,
               type=bool, default=True, require="Repo", ext=".gitignore")
OPTS.add_entry("Remote", "Remote url for git repository", action=actions.EXE,
               type=str, require="Repo", ext="git remote add origin {{Remote}}")
OPTS.group("UnitTests")
OPTS.add_entry("UnitTests", "Enable unit testing using Gtest",
               action=actions.FILE, type=bool, default=True, ext=[
                   ("test/Makefile", "{{Test}}/Makefile"),
                   ("external/Makefile", "{{External}}/Makefile")])
OPTS.add_entry("Test", "Test directory", default="test")
OPTS.add_entry("GTest", "Add google test as a submodule", type=bool,
               default=True, require="UnitTests",
               ext="git submodule add https://github.com/google/googletest {{External}}")
OPTS.group("Documentation")
OPTS.add_entry("Doc", "Add documentation to the project",
               type=bool, default=True)
OPTS.add_entry("DocDir", "Documentation directory", default="docs")
OPTS.add_entry("DocSys", "Documentation engine", type=str, default="None",
               choices={"None", "Sphinx", "MkDocs", "Doxygen"}, require="Doc")
OPTS.add_entry("Author", "Sphinx author", type=str,
               require=("DocSys", "Sphinx"))
OPTS.add_entry("Copyright", "Sphinx copyright",
               type=str, require=("DocSys", "Sphinx"))
GEN.languages.append(OPTS)
