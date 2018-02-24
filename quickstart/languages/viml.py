"""
Implements VimL Generator
"""

from quickstart.generator import GEN
from quickstart.entry import options, actions

OPTS = options("viml", "Vim Language")
OPTS.add_entry("Name", "Project name", type=str)
OPTS.add_entry("Description", "Project description", type=str)
OPTS.group("Directories")
OPTS.add_entry("Root", "Root directory", type=str, default=".")
OPTS.group("Git")
OPTS.add_entry("Repo", "Create a repository for the project",
               action=actions.EXE, type=bool, default=True, ext="git init .")
OPTS.add_entry("Ignore", "Create default git ignore file", action=actions.FILE,
               type=bool, default=True, require="Repo", ext=(".gitignore", ".gitignore"))
OPTS.add_entry("AddRemote", "Add remote repository", type=bool, default=True)
OPTS.add_entry("Remote", "Remote url for git repository", action=actions.EXE,
               type=str, require=("AddRemote", True), ext="git remote add origin {{Remote}}")
OPTS.group("Sections")
OPTS.add_entry("syntax", "Create syntax", type=bool, default=True,
               action=actions.FILE, ext=("syntax/source.vim", "syntax/{{Name}}.vim"))
OPTS.add_entry("ftdetect", "Create file type detection",
               type=bool, default=True, action=actions.FILE, ext=("ftdetect/source.vim", "ftdetect/{{Name}}.vim"))
OPTS.add_entry("ftplugin", "Create file type plugin", type=bool, default=True,
               action=actions.FILE, ext=("ftplugin/source/source.vim", "ftplugin/{{Name}}/{{Name}}.vim"))
OPTS.add_entry("indent", "Create indentation", type=bool, default=True,
               action=actions.FILE, ext=("indent/source.vim", "indent/{{Name}}/vim"))
OPTS.add_entry("autoload", "Create autoload", type=bool, default=True,
               action=actions.FILE, ext=("autoload/source.vim", "autoload/{{Name}}.vim"))
OPTS.add_entry("doc", "Create documentation", type=bool, default=True,
               action=actions.FILE, ext=("doc/source.txt", "doc/{{Name}}.txt"))
GEN.languages.append(OPTS)
