"""\
Clone a repository
"""

import shutil
import os
from buildkit import facilify

arg_specs = [
    dict(
        metavar='CLONE', 
        help_msg='the path to the repository to clone',
    ),
    dict(
        metavar='NEW_REPO_NAME',
        help_msg='name of the new repo',
    ),
]

def run(cmd):
    if not os.path.exists(os.path.join(cmd.args[0], 'conf')):
        cmd.err('The directory %r does not appear to be a repository')
        return 1
    dst = os.path.join(
        os.path.dirname(cmd.args[0]),
        cmd.args[1],
    )
    shutil.copytree(cmd.args[0], dst)

