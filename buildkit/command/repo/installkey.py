"""\
Install a GNUPG key for signing of packages in a repository
"""

#import uuid
import os
from buildkit import stacks
from buildkit.conf import DEFAULT_KEY_NAME, DEFAULT_KEY_EMAIL, DEFAULT_KEY_COMMENT

arg_specs = [
]

opt_specs_by_name = dict(
    name = dict(
        flags = ['--name'],
        help_msg = 'The name of the key, defaults to %r' % DEFAULT_KEY_NAME,
        metavar='NAME',
        default = DEFAULT_KEY_NAME,
    ),
    email = dict(
        flags = ['--email'],
        help_msg = 'The contact email, defaults to %r' % DEFAULT_KEY_EMAIL,
        metavar='EMAIL',
        default = DEFAULT_KEY_EMAIL,
    ),
    comment = dict(
        flags = ['--comment'],
        help_msg = 'An optional comment, defaults to %r' % DEFAULT_KEY_COMMENT,
        metavar='COMMENT',
        default = DEFAULT_KEY_COMMENT,
    ),
    #password = dict(
    #    flags = ['--password'],
    #    help_msg = 'A password for the key, defaults to a random uuid but you should probably set one explicitly',
    #    metavar='PASSWORD',
    #    default = uuid.uuid4(),
    #),
)

def run(cmd):
    # Check that there isn't already a key
    if cmd.repo.key_exists(
        cmd.parent.opts.key_dir, 
        cmd.parent.opts.base_repo_dir
    ):
        cmd.err(
            'Cannot install a new key because '
            'packages may have already been signed with the existing one'
        )
        return 1
    cmd_ = '. /usr/lib/buildkit/buildkit_common.sh\nbuildkit_ensure_public_key "%s" "%s" "%s" "%s" "%s"\nexit'%(
        cmd.opts.name,
        cmd.opts.email,
        cmd.opts.comment,
        #cmd.opts.password,
        cmd.parent.opts.key_dir,
        cmd.parent.opts.base_repo_dir,
    )
    cmd.out(cmd_)
    result = stacks.process(
        cmd_,
        # cwd=os.path.join(cmd.parent.opts.base_repo_dir, cmd.args[0]),
        shell=True,
        echo=True,
    )
    cmd.out(result.stdout)
    
