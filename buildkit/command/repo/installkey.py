"""\
Install a GNUPG key for signing of packages in a repository

Used like this:

::

    sudo rm -r /var/lib/buildkit/key
    sudo rm -r /var/lib/buildkit/repo/packages_public.key
    sudo buildkit repo installkey --email=name@example.com --name="Example Name" --comment="Example comment"

You can then see the result:

::

    okfn@coi-ckan-build:~/new/ckan$ sudo -u buildkit gpg --list-secret-keys --homedir /var/lib/buildkit/key
    /var/lib/buildkit/key/secring.gpg
    ---------------------------------
    sec   1024D/D8D8C238 2012-01-04
    uid                  Example Name (Example comment) <name@example.com>
    ssb   1024g/06DBEDB2 2012-01-04
    
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
    cmd_ = '. /usr/lib/buildkit/buildkit_common.sh\nbuildkit_ensure_public_key "%s" "%s" "%s" "%s" "%s"\nchown -R buildkit:buildkit /var/lib/buildkit/key\nchown buildkit:www-data /var/lib/buildkit/repo/packages_public.key\nexit'%(
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
    
