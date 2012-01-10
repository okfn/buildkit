"""\
Mount a disk image
"""

import os
import stacks
import sys

#
# Helpers
#

from .start import  get_vm_info, mount_image

arg_specs = [
    dict(
        metavar='NAME',
        help_msg='name of the VM image directory within /var/lib/buildkit/vm/',
    ),
]

opt_specs_by_name = dict(
    chroot = dict(
        flags=['-c', '--chroot'],
        help_msg='Also leave the terminal in a chroot within the mounted image',
    ),
)

def run(cmd):
    if os.geteuid() != 0:
        cmd.err("This script must be run as root")
        return 1
    vm_info = get_vm_info()
    found = True
    for instance in vm_info:
        if instance.image == cmd.args[0]:
            cmd.err('ERROR: The VM %r is still running'%cmd.args[0])
            return 2
    base = '/var/lib/buildkit/vm/'+cmd.args[0]+'/'
    if os.path.exists(base+'vmtmp/vm.info'):
        os.remove(base+'vmtmp/vm.info')
    mount_image(base+'disk.raw', base+'vmtmp')
    cmd.out('The VM is mounted at %r', base+'vmtmp')
    if cmd.opts.chroot:
        os.system('chroot %s'%base+'vmtmp')

