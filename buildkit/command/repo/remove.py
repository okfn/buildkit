"""\
Remove packages from a repository
"""

import os
from buildkit import facilify

arg_specs = [
    dict(
        metavar='REPO_DIR', 
        help_msg='the path to the repository',
    ),
    dict(
        metavar='PACKAGE_NAMES', 
        help_msg='the names of the packages to remove',
        min=0,
    ),
]
opt_specs_by_name = dict(
    key = dict(
        flags = ['-k', '--key'],
        help_msg = 'The key directory used to sign the packages',
        default='/var/lib/buildkit/key',
        metavar='KEYDIR',
    ),
    all = dict(
        flags = ['-a', '--all'],
        help_msg = 'Scan a directory to find the packages',
    ),
)

def run(cmd):
    package_names = cmd.args[1:]
    if cmd.opts.all:
        cmd_ = 'reprepro list lucid'
        result = facilify.process(
            cmd_,
            cwd=cmd.args[0],
            shell=True,
        )
        for line in result.stdout.split('\n'):
            if line.strip():
                info, name = line.split(':')
                name, version = name.strip().split(' ')
                if name not in package_names:
                    package_names.append(name)
    cmd_ = 'reprepro --gnupghome "%s" remove lucid %s' % (cmd.opts.key, ' '.join(package_names))
    cmd.out(cmd_)
    result = facilify.process(
        cmd_,
        cwd=cmd.args[0],
        shell=True,
    )
    cmd.out(result.stdout)
    
