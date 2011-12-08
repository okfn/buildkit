"""\
Add packages to a repository
"""

import os
from buildkit import stacks

arg_specs = [
    dict(
        metavar='REPO_NAME', 
        help_msg='The directory name of the repository',
    ),
    dict(
        metavar='PACKAGE_PATHS', 
        help_msg='One or more paths of packages to add',
        min=1,
    ),
]
opt_specs_by_name = dict(
    find_in = dict(
        flags = ['-a', '--all'],
        help_msg = 'Scan a directory to find the packages',
        metavar='PATH',
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
    packages = cmd.args[1:]
    abs_paths = []
    for package in packages:
        abs_paths.append(stacks.uniform_path(package))
    if cmd.opts.find_in:
        cmd_ = 'find "%s" | grep .deb$ | xargs --no-run-if-empty reprepro --gnupghome "%s" includedeb lucid %s' % (
            stacks.uniform_path(cmd.opts.find_in),
            cmd.parent.opts.key_dir,
            abs_paths and '"' + '" "'.join(abs_paths) + '"' or '',
        )
    else:
        cmd_ = ' '.join([
            'reprepro',
            '--gnupghome "%s"' % cmd.parent.opts.key_dir,
            'includedeb',
            'lucid',
        ] + abs_paths)
    cmd.out(cmd_)
    result = stacks.process(
        cmd_,
        cwd = os.path.join(cmd.parent.opts.base_repo_dir, cmd.args[0]),
        merge=True,
        shell=True,
    )
    cmd.out(result.stdout)
    
