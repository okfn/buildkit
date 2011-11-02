"""\
Create a virtual machine
"""

import os
import socket
from buildkit import facilify

arg_specs = [
    dict(
        metavar='VM_IP',
        help_msg='the VM\'s IP address, eg \'192.168.100.3\' or just \'3\' if you want to use 192.168.100 as the base IP (recommended)',
    ),
]

opt_specs_by_name = dict(
    proxy_ip = dict(
        flags=['-p', '--proxy-ip'],
        help_msg='the IP address of the apt proxy where packages can be downloaded, defauts to localhost',
        metavar='PROXY_IP',
    ),
    output_dir = dict(
        flags=['-o', '--output-dir'],
        help_msg='directory to place the generated virtual machine files, defaults to the current working directory',
        metavar='OUTPUT_DIR',
        default=os.getcwd(),
    ),
    base_name = dict(
        flags=['--basename'],
        help_msg='the name that forms the basis of the hostname, domain name and directory structures. Defaults to \'buildkit\'.',
        metavar='BASE_NAME',
        default='buildkit',
    ),
    packages = dict(
        flags=['-a', '--addpkg'],
        help_msg='install PACKAGE into the virtual machine too',
        metavar='PACKAGE',
        multiple=True,
    ),
)

def valid_ip(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not 0 <= int(part) <= 255:
            return False
    return True
 
def build(cmd, vm_ip_part, base_ip, arch, output_dir, proxy_ip=None, packages=None, base_name='buildkit'):
    if packages is None:
        packages = []
    # Need to check apt-proxy is set up on port 9999
    # http://127.0.0.1:9999/ubuntu/ gives "ERROR 403 - too few slashes in URI /ubuntu"
    args = dict(
        vm_ip_part=vm_ip_part,
        base_ip=base_ip,
        proxy_ip=proxy_ip,
        base_name=base_name,
        arch=arch,
    )
    cmd_ = """
    vmbuilder kvm ubuntu \
        --mem 512 \
        --cpus 1 \
        --domain %(base_name)s%(vm_ip_part)s \
        --dest %(base_name)s%(vm_ip_part)s \
        --flavour virtual \
        --suite lucid \
        --arch %(arch)s \
        --hostname %(base_name)s%(vm_ip_part)s \
        --user ubuntu \
        --pass ubuntu \
        --rootpass ubuntu \
        --debug -v \
        --ip %(base_ip)s.%(vm_ip_part)s \
        --mask 255.255.255.0 \
        --net %(base_ip)s.0 \
        --bcast %(base_ip)s.255 \
        --gw %(base_ip)s.254 \
        --dns %(base_ip)s.254 \
        --proxy http://%(proxy_ip)s:9999/ubuntu \
        --components main,universe \
        --addpkg openssh-server
    """%args
    for package in packages:
        cmd_ += '--addpkg '+package
    cmd.out(cmd_)
    result = facilify.process(
        cmd_,
        shell=True, 
        cwd=output_dir,
        merge=True,
        echo=True,
    )
    qcow2 = None
    new_output_dir = os.path.join(output_dir, "%(base_name)s%(vm_ip_part)s"%args)
    for filename in os.listdir(new_output_dir):
        if filename.endswith('.qcow2'):
            qcow2 = filename
    if not qcow2:
        cmd.err('Could not find a generated .qcow2 file')
        return 1
    dst = '%s/disk.raw'%(new_output_dir,)
    if not os.path.exists(dst):
        cmd.out('Generated %s', qcow2)
        cmd.out('Converting to raw ...')
        cmd_ = 'qemu-img convert -f qcow2 -O raw %s %s/disk.raw'%(qcow2, new_output_dir)
        cmd.out(cmd_)
        result = facilify.process(
            cmd_,
            shell=True,
            echo=True,
            cwd=new_output_dir,
        )
    else:
        cmd.err('Path %s already exists, not overwriting', dst)
    return result

def run(cmd):
    if not os.path.exists(cmd.opts.output_dir):
        os.mkdir(cmd.opts.output_dir)
    if cmd.opts.proxy_ip is None:
        proxy_ip = socket.gethostname()
    else:
        proxy_ip = cmd.opts.proxy_ip
        if not valid_ip(proxy_ip):
            cmd.err('Not a recognised IP address %r', proxy_ip)
            return 1
    vm_ip_part = cmd.args[0]
    if not '.' in vm_ip_part:
        vm_ip = '192.168.100.'+vm_ip_part
    else:
        vm_ip = vm_ip_part
        vm_ip_part = vm_ip.split('.')[-1]
    if not valid_ip(vm_ip):
        cmd.err('Not a recognised IP address %r', vm_ip)
        return 1
    if vm_ip_part in ['0','1','255','254']:
        cmd.err('The VM IP address cannot end with .%s', host_ip_part)
        return 1
    opts = facilify.str_keys(cmd.opts, ignore=['help', 'proxy_ip'])
    base_ip='.'.join(vm_ip.split('.')[:3])
    result = build(cmd, vm_ip_part, base_ip, proxy_ip=proxy_ip, arch=cmd.dist.determine_arch(), **opts)
    

