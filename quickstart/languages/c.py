"""
Implements C Generator
"""

from quickstart.generator import GEN
from quickstart.entry import options, actions

OPTS = options("c", "C")
OPTS.add_dir("{{Source}}")
OPTS.add_dir("{{DocDir}}")
OPTS.add_file("source/main.c", "{{Root}}/{{Source}}/main.c")
OPTS.add_file(".clang-format", "{{Root}}/.clang-format")
OPTS.add_file("Makefile", "{{Root}}/Makefile")
OPTS.add_file("source/Makefile", "{{Root}}/{{Source}}/Makefile")
OPTS.add_entry("Name", "Project name", type=str)
OPTS.add_entry("Description", "Project description", type=str)
OPTS.group("Directories")
OPTS.add_entry("Root", "Root directory", default=".")
OPTS.add_entry("Source", "Source directory", default="src")
OPTS.add_entry("Build", "Build directory", default="build")
OPTS.group("Git")
OPTS.add_entry("Repo", "Create a repository for the project",
               action=actions.EXE, type=bool, default=True, ext="git init .")
OPTS.add_entry("Ignore", "Create default git ignore file", action=actions.FILE,
               type=bool, default=True, require="Repo", ext=(".gitignore", ".gitignore"))
OPTS.add_entry("AddRemote", "Add remote repository",
               type=bool, default=True, require="Repo")
OPTS.add_entry("Remote", "Remote url for git repository", action=actions.EXE,
               type=str, require=("AddRemote", True), ext="git remote add origin {{Remote}}")
OPTS.group("Compiling")
OPTS.add_entry("CompSys", "Compiling system", type=str,
               default="None", choices={"Make", "Cmake"})
OPTS.add_entry("Compiler", "Compiler", type=str,
               default="gcc", choices={"cc", "gcc", "clang"})
OPTS.add_entry("Link", "Linked libraries", type=list)
OPTS.group("Documentation")
OPTS.add_entry("Doc", "Add documentation to the project",
               type=bool, default=True)
OPTS.add_entry("DocDir", "Documentation directory",
               default="docs", require="Doc")
OPTS.add_entry("DocSys", "Documentation engine", type=str, default="None",
               choices={"None", "Sphinx", "MkDocs", "Doxygen"}, require="Doc",
               action=actions.FILE, ext=[
                   ("Sphinx", "docs/Makefile", "{{DocDir}}/Makefile"),
                   ("Sphinx", "docs/source/conf.py",
                    "{{DocDir}}/source/conf.py"),
                   ("Sphinx", "docs/source/index.rst",
                    "{{DocDir}}/source/index.rst"),
                   ("MkDocs", "mkdocs.yml", "{{Root}}/mkdocs.yml"),
                   ("MkDocs", "docs/index.md", "{{DocDir}}/index.md"),
                   ("Doxygen", "Doxyfile", "{{Root}}/Doxyfile")
               ])
OPTS.add_entry("Author", "Sphinx author", type=str,
               require=("DocSys", "Sphinx"))
OPTS.add_entry("Copyright", "Sphinx copyright",
               type=str, require=("DocSys", "Sphinx"))
GEN.languages.append(OPTS)
