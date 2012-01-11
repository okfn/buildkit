"""\
Connect to the serial terminal of a running VM
"""

import os
import stacks
import sys

#
# Helpers
#

from .status import full_info

arg_specs = [
    dict(
        metavar='NAME',
        help_msg='name of the VM image directory within /var/lib/buildkit/vm/',
    ),
]

opt_specs_by_name = dict(
)

def run(cmd):
    if os.geteuid() != 0:
        cmd.err("This script must be run as root")
        return 1
    result = full_info([cmd.args[0]])
    if result.error:
        cmd.err(result.error)
        return 2
    serial = result.instances[0].serial
    cmd.out('Connecting to %r ...', serial)
    result = stacks.process(
        [
            'socat', '-', serial,
        ],
        in_data = '\n\n',
    )


