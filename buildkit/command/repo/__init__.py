"""\
Manage a repository of Debian packages
"""

import os
from buildkit import stacks
from buildkit.conf import BASE_REPO_DIR, BASE_KEY_DIR

arg_specs = []
opt_specs_by_name = {
    'base_repo_dir': dict(
        flags = ['-b', '--base-repo-dir'],
        help_msg = 'The directory where all the repos are stored, defaults to %r' % BASE_REPO_DIR,
        metavar = 'REPO_DIR',
        default = BASE_REPO_DIR,
    ),
    'key_dir': dict(
        flags = ['-k', '--key'],
        help_msg = 'The key directory used to sign the packages, defaults to %r' % BASE_KEY_DIR,
        default=BASE_KEY_DIR,
        metavar='KEY_DIR',
    ),
}
child_command_specs = stacks.find_commands(__package__, os.path.dirname(__file__))
help_template = stacks.main_help_template

def run(cmd):
    return 0

