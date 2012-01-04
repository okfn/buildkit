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
        metavar='PACKAGE_NAME', 
        help_msg='Name of one or more packages to remove (without their version numbers, file extensions or anything else) for example: python-buildkit rsync etc. Not needed if --all is used',
        min=0,
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
    if not package_names:
        cmd.err('ERROR: No packages to remove')
        return 1
    cmd_ = 'reprepro --gnupghome "%s" remove lucid %s' % (cmd.parent.opts.key_dir, ' '.join(package_names))
    cmd.out(cmd_)
    result = stacks.process(
        cmd_,
        cwd=os.path.join(cmd.parent.opts.base_repo_dir, cmd.args[0]),
        shell=True,
    )
    cmd.out(result.stdout)
    
