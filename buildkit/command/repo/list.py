"""\
List packages in a repository
"""

import os
from buildkit import stacks

arg_specs = [
    dict(
        metavar='REPO_NAME', 
        help_msg='The directory name of the repository',
    ),
]
opt_specs_by_name = dict(
)

def run(cmd):
    # Check that a key is installed
    if not cmd.repo.key_exists(
        cmd.parent.opts.key_dir, 
        cmd.parent.opts.base_repo_dir
    ):
        cmd.err(
            'No repo key has ben set up, please run `buildkit repo '
            'installkey\' to install one'
        )
        return 1
    cmd_ = 'reprepro list lucid'
    result = stacks.process(
        cmd_,
        cwd=os.path.join(cmd.parent.opts.base_repo_dir, cmd.args[0]),
        shell=True,
        merge=True,
    )
    cmd.out(result.stdout.strip())
    
