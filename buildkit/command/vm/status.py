"""\
List running virtual machines
"""

import os
import stacks
import sys

#
# Helpers
#

from .start import  get_vm_info

arg_specs = [
]

opt_specs_by_name = dict(
)

def parse_vm_info(image):
    path = '/var/lib/buildkit/vm/%s/vmtmp/vm.info'%image
    if os.path.exists(path):
        fp = open(path, 'r')
        data = fp.read().split('\n')
        fp.close()
        return stacks.obj(
            pid = data[0],
            serial = data[1],
            monitor = data[2],
        )
    else:
        return stacks.obj(
            pid = None,
        )

def run(cmd):
    if os.geteuid() != 0:
        cmd.err("This script must be run as root")
        return 1
    vm_info = get_vm_info()
    if not vm_info:
        cmd.out('No VMs running')
    else:
        spec = '%-6s %-20s %-8s %-12s %-12s'
        cmd.out(spec, 'PID', 'Image', 'Tunnel', 'Serial', 'Monitor')
        for instance in vm_info:
            info = parse_vm_info(instance.image)
            if instance.pid != info.pid:
                instance['serial'] = 'UNKNOWN' 
                instance['monitor'] = 'UNKNOWN'
            else:
                instance.update(info)
            cmd.out(
                spec,
                instance.pid, 
                instance.image, 
                instance.tunnel, 
                instance.serial, 
                instance.monitor,
            )

