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
    dict(
        metavar='NAME',
        help_msg='names of the VM image directory within /var/lib/buildkit/vm/',
        min=0,
    ),
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

def full_info(images=None):
    if images == []:
        images = None
    vm_info = get_vm_info()
    error = None
    instances = []
    if not vm_info:
        error = 'No VMs running'
    else:
        not_running = images[:]
        for instance in vm_info:
            if images is None or instance.image in images:
                info = parse_vm_info(instance.image)
                if instance.pid != info.pid:
                    instance['serial'] = 'UNKNOWN' 
                    instance['monitor'] = 'UNKNOWN'
                else:
                    instance.update(info)
                instances.append(instance)
                not_running.pop(not_running.index(instance.image))
    if images is not None and not_running:
        error = 'The following VMs are not running: %r'%(', '.join(not_running))
    return stacks.obj(
        error=error,
        instances=instances,
    )

def run(cmd):
    if os.geteuid() != 0:
        cmd.err("This script must be run as root")
        return 1
    result = full_info(cmd.args)
    if result.error:
        cmd.err(result.error)
        return 2
    spec = '%-6s %-20s %-8s %-12s %-12s'
    cmd.out(spec, 'PID', 'Image', 'Tunnel', 'Serial', 'Monitor')
    for instance in result.instances:
        cmd.out(
            spec,
            instance.pid, 
            instance.image, 
            instance.tunnel, 
            instance.serial, 
            instance.monitor,

        )

