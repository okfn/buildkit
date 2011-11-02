"""\
Create distribution packages
"""

import os
from buildkit import facilify

arg_specs = []
child_command_specs = facilify.find_commands(__package__, os.path.dirname(__file__))
help_template = facilify.main_help_template

def run(cmd):
    return 0

