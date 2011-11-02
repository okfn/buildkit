"""\
Add packages to a repository
"""

import os
from buildkit import facilify

arg_specs = [
    dict(
        metavar='REPO_DIR', 
        help_msg='the path to the repository',
    ),
    dict(
        metavar='PACKAGE_PATHS', 
        help_msg='zero or more paths of packages to add',
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
    find_in = dict(
        flags = ['-a', '--all'],
        help_msg = 'Scan a directory to find the packages',
        metavar='PATH',
    ),
)

def run(cmd):
    packages = cmd.args[1:]
    abs_paths = []
    for package in packages:
        abs_paths.append(facilify.uniform_path(package))
    if cmd.opts.find_in:
        cmd_ = 'find "%s" | grep .deb$ | xargs --no-run-if-empty reprepro --gnupghome "%s" includedeb lucid %s' % (
            facilify.uniform_path(cmd.opts.find_in),
            cmd.opts.key,
            abs_paths and '"' + '" "'.join(abs_paths) + '"' or '',
        )
    else:
        cmd_ = ' '.join([
            'reprepro',
            '--gnupghome "%s"' % cmd.opts.key,
            'includedeb',
            'lucid',
        ] + abs_paths)
    cmd.out(cmd_)
    result = facilify.process(
        cmd_,
        cwd = cmd.args[0],
        merge=True,
        shell=True,
    )
    cmd.out(result.stdout)
    
