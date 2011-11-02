"""\
List packages in a repository
"""

import os
from buildkit import facilify

arg_specs = [
    dict(
        metavar='REPO_DIR', 
        help_msg='the path to the repository',
    ),
]
opt_specs_by_name = dict(
)

def run(cmd):
    cmd_ = 'reprepro list lucid'
    result = facilify.process(
        cmd_,
        cwd=cmd.args[0],
        shell=True,
        merge=True,
    )
    cmd.out(result.stdout.strip())
    
