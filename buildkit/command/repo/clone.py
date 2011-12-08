"""\
Clone a repository
"""

import shutil
import os
from buildkit import stacks

arg_specs = [
    dict(
        metavar='CLONE', 
        help_msg='the name of the repository to clone',
    ),
    dict(
        metavar='NEW_REPO_NAME',
        help_msg='name of the new repo',
    ),
]

def run(cmd):
    src = stacks.uniform_path(
        os.path.join(
            cmd.parent.opts.base_repo_dir, 
            cmd.args[0],
        )
    )
    if not os.path.exists(os.path.join(src, 'conf')):
        cmd.err('The directory %r does not appear to be a repository', src)
        return 1
    dst = os.path.join(
        cmd.parent.opts.base_repo_dir,
        cmd.args[1],
    )
    shutil.copytree(src, dst)
    cmd.out('done.')

