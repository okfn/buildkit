"""\
Clone a virtual machine
"""

import os
import stacks
import sys
import shutil

def clone(src, dst):
    if '/' in src:
        raise Exception('The src argument cannot contain a / character')
    if '/' in dst:
        raise Exception('The dst argument cannot contain a / character')
    result = stacks.process(
        [
            'sudo', '-u', 'buildkit', 
            'cp',  '-pr', '/var/lib/buildkit/vm/%s'%src, '/var/lib/buildkit/vm/%s'%dst,
        ],
    )
    return result

#
# Command
#

arg_specs = [
    dict(
        metavar='SRC_NAME',
        help_msg='Name of the source VM image directory within /var/lib/buildkit/vm/',
    ),
    dict(
        metavar='DST_NAME',
        help_msg="Name of the destination directory",
    ),
]

opt_specs_by_name = dict(
)

def run(cmd):
    if not os.path.exists(os.path.join('/var/lib/buildkit/vm', cmd.args[0])):
        cmd.err('No such directory %r', os.path.join('/var/lib/buildkit/vm', cmd.args[0]))
        return 1
    if  os.path.exists(os.path.join('/var/lib/buildkit/vm', cmd.args[1])):
        cmd.err('The directory %r already exists', os.path.join('/var/lib/buildkit/vm', cmd.args[1]))
        return 2
    clone(cmd.args[0], cmd.args[2])
    cmd.out('done.')

