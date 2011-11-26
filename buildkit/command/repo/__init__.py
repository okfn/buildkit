"""\
Manage a repository of Debian packages
"""

import os
from buildkit import stacks

arg_specs = []
child_command_specs = stacks.find_commands(__package__, os.path.dirname(__file__))
help_template = stacks.main_help_template

def run(cmd):
    return 0

