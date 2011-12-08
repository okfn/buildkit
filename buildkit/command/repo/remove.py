"""\
Remove packages from a repository
"""

import os
from buildkit import stacks

arg_specs = [
    dict(
        metavar='REPO_NAME', 
        help_msg='The directory name of the repository',
    ),
    dict(
        metavar='PACKAGE_NAMES', 
        help_msg='Names of the packages to remove',
        min=1,
    ),
]
opt_specs_by_name = dict(
    all = dict(
        flags = ['-a', '--all'],
        help_msg = 'Scan a directory to find the packages',
    ),
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
    package_names = cmd.args[1:]
    if cmd.opts.all:
        cmd_ = 'reprepro list lucid'
        result = stacks.process(
            cmd_,
            cwd=os.path.join(cmd.parent.opts.base_repo_dir, cmd.args[0]),
            shell=True,
        )
        for line in result.stdout.split('\n'):
            if line.strip():
                info, name = line.split(':')
                name, version = name.strip().split(' ')
                if name not in package_names:
                    package_names.append(name)
    cmd_ = 'reprepro --gnupghome "%s" remove lucid %s' % (cmd.parent.opts.key_dir, ' '.join(package_names))
    cmd.out(cmd_)
    result = stacks.process(
        cmd_,
        cwd=os.path.join(cmd.parent.opts.base_repo_dir, cmd.args[0]),
        shell=True,
    )
    cmd.out(result.stdout)
    
