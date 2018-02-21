"""
Implements Python Generator
"""

from generator import GEN
from entry import options, actions

OPTS = options("python", "Python")
OPTS.add_entry("Name", "Project name", type=str)
OPTS.add_entry("Description", "Project description", type=str)
GEN.languages.append(OPTS)
