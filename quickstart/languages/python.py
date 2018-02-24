"""
Implements Python Generator
"""

from quickstart.generator import GEN
from quickstart.entry import options, actions

OPTS = options("python", "Python")
OPTS.add_entry("Name", "Project name", type=str)
OPTS.add_entry("Description", "Project description", type=str)
OPTS.group("Git")
OPTS.add_entry("Repo", "Create a repository for the project",
               action=actions.EXE, type=bool, default=True, ext="git init .")
OPTS.add_entry("Ignore", "Create default git ignore file", action=actions.FILE,
               type=bool, default=True, require="Repo", ext=(".gitignore", ".gitignore"))
OPTS.add_entry("AddRemote", "Add remote repository",
               type=bool, default=True, require="Repo")
OPTS.add_entry("Remote", "Remote url for git repository", action=actions.EXE,
               type=str, require=("AddRemote", True), ext="git remote add origin {{Remote}}")
OPTS.group("Config")
OPTS.add_entry("PyEnv", "Enable PyEnv", type=bool, default=True)
OPTS.add_entry("PyV", "Python Version", type=str, default="3.6.4", choices={
               "2.4", "2.5", "2.7", "3.1", "3.2", "3.3.0", "3.4.0", "3.5.0", "3.6.0", "3.6.4", "3.7-dev"},
               require="PyEnv")
OPTS.group("UnitTests")
OPTS.add_entry("UnitTests", "Enable unit testing using PyTest",
               type=bool, default=True)
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
