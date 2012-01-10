"""\
Stop a virtual machine. Only works if they respond to an ACPI system powerdown message.
"""

import os
import stacks
import sys
import time

from .start import get_vm_info
from .status import parse_vm_info

arg_specs = [
    dict(
        metavar='NAME',
        help_msg='name of the VM image directory within /var/lib/buildkit/vm/',
    ),
]

opt_specs_by_name = dict(
    wait = dict(
        flags=['--wait'],
        help_msg='Wait for shutdown to complete before returning',
    ),
)

def run(cmd):
    if os.geteuid() != 0:
        cmd.err("This script must be run as root")
        return 1
    vm_info = get_vm_info()
    vm = None
    for instance in vm_info:
        if instance.image == cmd.args[0]:
            vm = instance
    if vm is None:
        cmd.err('VM %r is not running'%cmd.args[0])
        return 1
    pts_info = parse_vm_info(vm.image)
    if not pts_info.pid:
        cmd.err('Could not obtain the monitor information for %r.'%cmd.args[0])
        cmd.err('If can log in to the machine you should shut it down manually. Otherwise if you know the correct char device you can stop it like this:')
        cmd.err('    $ echo "system_powerdown" | sudo socat - /dev/pts/XX')
        cmd.err('Failing that you could forcibly kill the VMs pid %r', vm.pid)
        return 2
    stacks.process(
        'echo "system_powerdown" | sudo socat - %s'%pts_info.monitor,
        shell=True,
    )
    cmd.out('System powerdown command sent.')
    if cmd.opts.wait:
        cmd.out('Waiting for shutdown to complete .', end='')
        wait = True
        while wait:
            time.sleep(5)
            vm_info = get_vm_info()            
            found = False
            cmd.out('.', end='')
            for instance in vm_info:
                if cmd.args[0] == instance.image:
                    found=True
                    break
            if not found:
                wait=False
        cmd.out('\nShutdown complete.')
   

