"""\
Copy all the packages from a repository into a directory
"""

import os
import shutil
from buildkit import facilify

arg_specs = [
    dict(
        metavar='REPO_DIR', 
        help_msg='the path to the repository',
    ),
]
opt_specs_by_name = dict(
    output_dir = dict(
        flags=['-o', '--output-dir'],
        help_msg='directory to place the generated virtual machine files, defaults to the current working directory',
        metavar='OUTPUT_DIR',
        default=os.getcwd(),
    ),
)

def run(cmd):
    cmd_ = 'find . | grep .deb'
    result = facilify.process(
        cmd_,
        cwd=cmd.args[0],
        shell=True,
        merge=True,
    )
    for line in result.stdout.strip().split():
        src = os.path.join(cmd.args[0], line.strip())
        dst = os.path.join(cmd.opts.output_dir, line.split('/')[-1])
        cmd.out(src)
        shutil.copyfile(src, dst)
    
