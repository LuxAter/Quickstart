"""
Implements C++ Generator
"""

from quickstart.generator import GEN
from quickstart.entry import options, actions

OPTS = options("cpp", "C++")
OPTS.add_dir("{{Source}}")
OPTS.add_dir("{{Include}}")
OPTS.add_dir("{{External}}")
OPTS.add_dir("{{DocDir}}")
OPTS.add_file("source/main.cpp", "{{Root}}/{{Source}}/main.cpp")
OPTS.add_file(".clang-format", "{{Root}}/.clang-format")
OPTS.add_file("Makefile", "{{Root}}/Makefile")
OPTS.add_file("source/Makefile", "{{Root}}/{{Source}}/Makefile")
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
               type=bool, default=True, require="Repo", ext=(".gitignore", ".gitignore"))
OPTS.add_entry("AddRemote", "Add remote repository",
               type=bool, default=True, require="Repo")
OPTS.add_entry("Remote", "Remote url for git repository", action=actions.EXE,
               type=str, require=("AddRemote", True), ext="git remote add origin {{Remote}}")
OPTS.group("Compiling")
OPTS.add_entry("CompSys", "Compiling system", type=str,
               default="None", choices={"Make", "Cmake"})
OPTS.add_entry("Compiler", "Compiler", type=str,
               default="g++", choices={"g++", "clang++"})
OPTS.add_entry("CPPV", "C++ version", type=str, default="c++11",
               choices={"c++11", "c++14", "c++17"})
OPTS.add_entry("Link", "Linked libraries", type=list)
OPTS.group("UnitTests")
OPTS.add_entry("UnitTests", "Enable unit testing using Gtest",
               action=actions.FILE, type=bool, default=True, ext=[
                   ("test/tmp.cpp", "{{Test}}/tmp.cpp"),
                   ("test/Makefile", "{{Test}}/Makefile"),
                   ("external/Makefile", "{{External}}/Makefile")])
OPTS.add_entry("Test", "Test directory", default="test")
OPTS.add_entry("GTest", "Add google test as a submodule", type=bool,
               default=True, require="UnitTests",
               ext="git submodule add https://github.com/google/googletest {{External}}")
OPTS.group("Continuouse Integration")
OPTS.add_entry("CI", "Enable continuous integration services",
               type=bool, default=True)
OPTS.add_entry("CISys", "Continuouse integration service", type=str,
               default="None", choices={"Travis", "Jenkins", "Circle"}, require="CI",
               action=actions.FILE, ext=[("Travis", "travis.yml", ".travis.yml")])
OPTS.add_entry("CIapt", "Install from apt", type=list, require="CI")
OPTS.add_entry("CIpip", "Install from pip", type=list, require="CI")
OPTS.add_entry("Cov", "Enable code coverage",
               type=bool, default=True, require="CI")
OPTS.add_entry("CovSye", "Code coverage service", type=str,
               default="None", choices={"None", "CodeCov", "Coveralls"}, require="Cov")
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
                   ("Doxygen", "Doxyfile", "{{Roor}}/Doxyfile")
               ])
OPTS.add_entry("Author", "Sphinx author", type=str,
               require=("DocSys", "Sphinx"))
OPTS.add_entry("Copyright", "Sphinx copyright",
               type=str, require=("DocSys", "Sphinx"))
GEN.languages.append(OPTS)
