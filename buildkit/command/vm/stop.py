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
    dont_wait = dict(
        flags=['--dont-wait'],
        help_msg='Return immediately without waiting for shutdown to complete',
    ),
    no_console = dict(
        flags=['--no-console'],
        help_msg='Don\'t show boot output during start up',
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
    cmd.out('Sending system powerdown command ...')
    stacks.process(
        'echo "system_powerdown" | sudo socat - %s'%pts_info.monitor,
        shell=True,
    )
    cmd.out('done.')
    if not cmd.opts.dont_wait:
        serial = pts_info.serial
        if serial != 'UNKNOWN':
            def err(fh, stdin, output, exit):
                pass
            def out(fh, stdin, output, exit):
                while not exit:
                    line = fh.readline()
                    if not cmd.opts.no_console:
                        cmd.out(line, end='')
                    output.write(line)
                    if 'Power down.' in line:
                        cmd.out("Found the wait message, exiting ...")
                        exit.append(0)
            if not cmd.opts.no_console:
                cmd.out('Connecting to the VM serial console ...')
            result = stacks.process(
                [
                    'socat', '-', serial,
                ],
                out=out,
                err=err,
            )
            cmd.out('done.')
        cmd.out('Waiting for shutdown to complete ...', end='')
        wait = True
        while wait:
            vm_info = get_vm_info()            
            found = False
            cmd.out('.', end='')
            for instance in vm_info:
                if cmd.args[0] == instance.image:
                    found=True
                    break
            if not found:
                wait=False
            else:
                time.sleep(2)
        cmd.out('\nShutdown complete.')
   

