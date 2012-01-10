"""\
Start a virtual machine

eg:

    buildkit-vm-start eth1 qtap0 1024M 4 ckan -nographic

"""

#  To get dmesg output on boot:
#
#  cat << EOF | sudo tee /boot/grub/menu.lst
#  title           Ubuntu 10.04.3 LTS, kernel 2.6.32-33-server
#  uuid            cebcbb77-a2bf-4bb8-b1b3-1323f27ac7a4
#  -1323f27ac7a4 ro console=ttyS0,115200n8 console=tty0
#  initrd          /boot/initrd.img-2.6.32-33-server
#  
#  title           Ubuntu 10.04.3 LTS, kernel 2.6.32-33-server (recovery mode)
#  uuid            cebcbb77-a2bf-4bb8-b1b3-1323f27ac7a4
#  -1323f27ac7a4 ro  single
#  initrd          /boot/initrd.img-2.6.32-33-server
#  EOF
#
#  Something like this might work too:
#  
#  cat << EOF | sudo tee /etc/default/grub 
#  GRUB_CMDLINE_LINUX="console=ttyS0,38400n8 console=tty0"
#  EOF
#  
#  sudo update-grub
# 
#  For shutdown support:
# 
#  sudo aptitude install acpid acpi-support


import os
import socket
import stacks
import pwd
import grp
import sys
import shutil
import stat

#
# Helpers
#

def gen_tunnel(bridge_name):
    bridge_info = get_bridge_info()
    tunnels = bridge_info.bridges[bridge_name]
    vm_info = get_vm_info()
    used = []
    for instance in vm_info:
        used.append(instance.tunnel)
    for tunnel in tunnels:
        if tunnel not in used:
            print "Re-using tunnel %r"%tunnel
            return tunnel
    if not tunnels:
        print "New tunnel qtap0"
        return 'qtap0'
    else:
        new_tunnel = 'qtap'+str(int(tunnels[-1][4:])+1)
        print "New tunnel %r"%new_tunnel
        return new_tunnel

def determine_ip():
    result = stacks.process(
        "/sbin/ifconfig $NETWORK_DEVICE | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}' | grep -v '127.0.0.1' | grep -v '192.168.100.' | grep -v '192.168.122.1'",
        shell=True
    )
    exception = Exception('Could not determine the IP address, is the host connected to the internet? If so, please --ip option to specify the IP address manually')
    if result.retcode:
        raise exception
    ip = result.stdout.strip().split('\n')[0]
    if not valid_ip(ip):
        raise exception
    return ip

def gen_mac():
    result = stacks.process(
        r"dd if=/dev/urandom count=1 2>/dev/null | md5sum | sed 's/^\(..\)\(..\)\(..\)\(..\).*$/\1:\2:\3:\4/'",
        shell=True,
    )
    if result.retcode:
        raise Exception('Could not generate a mac address automatically, please use the --mac-address option')
    mac = '52:54:'+result.stdout.strip()
    return mac

def determine_interface(ip):
    result = stacks.process(
        "/sbin/ifconfig | grep -B 1 '%s' | grep -v '%s' | awk '{ print $1}'"%(ip, ip),
        shell=True,
    )
    if result.retcode:
        raise Exception('Could not determine the interface automatically, please use the --interface option')
    interface = result.stdout.strip()
    return interface

def valid_ip(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not 0 <= int(part) <= 255:
            return False
    return True

def start_apt_cacher_ng_if_not_running():
    cmd = '''\
APTCACHERNG=`ps aux | grep /usr/sbin/apt-cacher | grep -v grep`
if [ ! "$APTCACHERNG" ] ; then
    echo "Starting apt-cacher-ng ..."
    /etc/init.d/apt-cacher-ng start
    echo "done."
fi
'''
    result = stacks.process(cmd, shell=True, echo=True)
    return result

def get_vm_info():
    cmd = 'ps ax -o "pid args" | grep "/bin/kvm" | grep "/var/lib/buildkit/vm"'
    result = stacks.process(
        cmd=cmd,
        shell = True,
    )
    lines = result.stdout.split('\n')
    instances = []
    for line in lines:
        if not line.strip() or cmd in line:
            continue
        parts = [part for part in line.strip().split(' ') if part]
        pid = parts[0]
        try:
            image_arg = parts[18].split('=')[1].split(',')[0].split('/')[-2]
        except:
            image_arg = 'ERROR'
        try:
            net_arg = parts[22].split(',')[1].split('=')[1]
        except:
            net_arg = 'ERROR'
        instance = stacks.obj(
            pid = pid,
            image = image_arg,
            tunnel = net_arg 
        )
        instances.append(instance)
    return instances

def get_bridge_info():
    result = stacks.process(
        [
            'brctl', 'show',
        ],
    )
    lines = result.stdout.split('\n')
    interfaces_pos = lines[0].find('interfaces')
    tunnels = []
    bridges = stacks.obj()
    bridge = None
    for line in lines[1:]:
        new_bridge = line.split('\t')[0].strip()
        if new_bridge:
            bridge = new_bridge
        if not bridges.has_key(bridge):
            bridges[bridge] = []
        tunnel = line.split('\t')[-1]
        if tunnel:
            bridges[bridge].append(tunnel)
            tunnels.append(tunnel)
    tunnels.sort()
    return stacks.obj(bridges=bridges, tunnels=tunnels)

def create_bridge(interface, bridge_name, add=False):
    cmd = "iptables -t nat -A POSTROUTING -o %s -j MASQUERADE" % interface
    if add:
        cmd += '\nbrctl addbr %s'%bridge_name
    cmd += '\nifconfig %s 192.168.100.254 netmask 255.255.255.0 up'%bridge_name
    cmd += '\necho "1" > /proc/sys/net/ipv4/ip_forward'
    result = stacks.process(cmd, shell=True, echo=True)
    return result

def create_tunnel(tunnel):
    cmd = '''\
modprobe tun
tunctl -b -u root -t %(tunnel)s
brctl addif br0 %(tunnel)s
ifconfig %(tunnel)s up 0.0.0.0 promisc'''%dict(tunnel=tunnel)
    result = stacks.process(cmd, shell=True, echo=True)
    return result

def buildkit_apt_cache_installed():
    cmd = '''dpkg -l | grep "ii  buildkit-apt-cache"'''
    result = stacks.process(cmd, shell=True, echo=True)
    if result.stdout.strip():
        return True
    return False
    
def update_image(image, host_ip, use_apt_proxy=True):
    path = "/var/lib/buildkit/vm/%s/vmtmp"%image
    shutil.copyfile('/etc/resolv.conf', os.path.join(path, 'etc/resolv.conf'))
    fp =open(os.path.join(path, 'etc/apt/apt.conf'), 'w')
    if use_apt_proxy:
    	fp.write('Acquire::http { Proxy \"http://%s:3142/ubuntu\"; };'%host_ip)
    else:
    	fp.write('')
    fp.close()
    fp = open(os.path.join(path, 'etc/buildkit_host_ip'), 'w')
    fp.write(host_ip) 
    fp.close()
    fp = open(os.path.join(path, 'etc/hosts'), 'r')
    to_write = []
    found = False
    for line in fp.read().split('\n'):
        if 'host.buildkit' in line:
            if not found:
                found = True
                to_write.append("%s host.buildkit"%host_ip)
        else:
            to_write.append(line)
    if not found:
        to_write.append("%s host.buildkit"%host_ip)
    fp.close()
    fp = open(os.path.join(path, 'etc/hosts'), 'w')
    fp.write('\n'.join(to_write))
    fp.close()
    fp = open(os.path.join(path, 'etc/init.d/buildkit_exec'), 'w')
    fp.write('''\
#! /bin/sh
# /etc/init.d/buildkit_exec
#

# Carry out specific functions when asked to by the system
case "$1" in
  start)

    if [ -e "/etc/buildkit_on_start.sh" ] ; then
        echo "Running custom buildkit on start script ..."
        bash /etc/buildkit_on_start.sh
        echo "done."
    fi
    ;;
  stop)
    ;;
  *)
    echo "Usage: /etc/init.d/blah {start|stop}"
    exit 1
    ;;
esac

exit 0
''')
    fp.close()
    os.chmod(os.path.join(path, 'etc/init.d/buildkit_exec'), stat.S_IEXEC)
    link_path = os.path.join(path, 'etc/rc2.d/S99buildkit_exec')
    if os.path.lexists(link_path):
        os.remove(link_path)
    os.symlink(
        '../init.d/buildkit_exec',
        link_path,
    )

    fp = open(os.path.join(path, 'etc/init/ttyS0.conf'), 'w')
    fp.write('''\
# ttyS0 - getty
#
# This service maintains a getty on ttyS0 from the point the system is
# started until it is shut down again.

start on stopped rc RUNLEVEL=[2345]
stop on runlevel [!2345]

respawn
exec /sbin/getty -L 38400 ttyS0 vt102
''')
    fp.close()

def mount_image(image, path):
    if not os.path.exists(path):
        os.mkdir(path)
        uid = pwd.getpwnam('buildkit')[2]
        gid = grp.getgrnam('buildkit')[2]
        os.chown(path, uid, gid)
    files = os.listdir(path)
    if files:
        if len(files) > 1:
            # Must be mounted
            umount_image(path)
        elif len(files) > 0 and files[0] == 'vm.info':
            os.remove(os.path.join(path, 'vm.info'))
        else:
            raise Exception('The %r directory is not empty'%path)
    result = stacks.process(
        'mount -t ext4 -o loop,offset=512 %s %s'%(image, path),
        shell=True,
    )
    if result.retcode:
        raise Exception('Could not mount the image %s. %s\n'%(image, result.stderr))

def umount_image(path):
    result = stacks.process(
        'umount %s'%path,
        shell=True,
    )
    if result.retcode:
        raise Exception('Could not unmount the image %s. %s\n'%(image, result.stderr))


#
# Converters
#

def check_apt_proxy_available(value):
    if value is True:
        if not buildkit_apt_cache_installed():
            raise Exception('Cannot use apt-proxy functionality because \'buildkit-apt-cache\' is not installed')
    return value 

def get_ip_if_missing(ip):
    if ip is None:
        ip = determine_ip()
    return ip

def gen_mac_if_missing(mac):
    if mac is None:
        mac = gen_mac()
    return mac

#def gen_tunnel_if_missing(key, data, errors, context):
#    tunnel = data[key]
#    if tunnel is None:
#        tunnel = gen_tunnel(data[stacks.sibling_key(key, 'bridge_name')])
#    data[key] = tunnel

def parse_file_and_dir_specs(value):
    result = []
    for spec in value:
        pair = spec.split('->')
        if not len(pair) == 2:
            raise Exception('A spec can only contain one set of -> characters')
        src = stacks.uniform_path(pair[0].strip())
        if not os.path.exists(src):
            raise Exception('No such file or directory %r'%src)
        dst = pair[1].strip()
        if not dst.startswith('/'):
            raise Exception('The destination path must start with a / character')
        result.append(stacks.obj(src=src, dst=dst))
    return result

def parse_dir_specs(value):
    specs = parse_file_and_dir_specs(value)
    for spec in specs:
        if not os.path.isdir(spec.src):
            raise Exception('Path %r is not a directory'%spec.src)
        #if spec.dest.endswith('/'):
        #    spec.dest = os.path.join(
        #        spec.dest,
        #        spec.src.split('/')[-1]
        #    )
    return specs

def parse_file_specs(value):
    specs = parse_file_and_dir_specs(value)
    for spec in specs:
        if not os.path.isfile(spec.src):
            raise Exception('Path %r is not a file'%spec.src)
        if spec.dst.endswith('/'):
            spec.dst = os.path.join(
                spec.dest,
                spec.src.split('/')[-1]
            )
    return specs


#
# Command
#

arg_specs = [
    dict(
        metavar='NAME',
        help_msg='name of the VM image directory within /var/lib/buildkit/vm/',
    ),
    dict(
        metavar='KVMARGS',
        help_msg="Any extra arguments to pass to KVM eg '-nographic' if you are running on a server",
        min=0,
    ),
]

opt_specs_by_name = dict(
    cpus = dict(
        flags=['-c', '--cpus'],
        help_msg='Number of Physical CPUs to give to the VM, cannot be more than the number of CPUs the physical host has. Defaults to \'1\'',
        metavar='NUM',
        default='1',
    ),
    mem = dict(
        flags=['-m', '--mem'],
        help_msg='Amout of memory to give the VM. Defaults to \'512M\'',
        metavar='MEMORY',
        default='512M',
    ),
    ip = dict(
        flags=['-i', '--ip'],
        help_msg='IP address of host machine (used in routing to the internet for the VMs)',
        metavar='HOST_IP',
        converter=[get_ip_if_missing],
    ),
    bridge_name = dict(
        flags=['-b', '--bridge'],
        help_msg='Name of bridge to create/use. Defaults to \'br0\'.',
        metavar='NAME',
        default='br0',
    ),
    tunnel = dict(
        flags=['-t', '--tunnel-prefix'],
        help_msg='Name of the tunnel to use for this VM. If not specified, the first available tunnel starting \'qtap\' will be used, eg \'qtap0\'.',
        metavar='NAME',
        #converter=[gen_tunnel_if_missing],   
    ),
    copy_dir = dict(
        flags=['-d', '--copy-dir'],
        help_msg='Copy a directory into the VM before it boots, removing the directory if it already exists. DIR_SPEC should be in the format \'SRC -> DST\' where SRC is the source path to the file and DST is the full destination path on the VM drive, begining with a / character.',
        metavar='DIR_SPEC',
        multiple=True,
        converter=[parse_dir_specs],
    ),
    copy_file = dict(
        flags=['-f', '--copy-file'],
        help_msg='Copy a file into the VM before it boots. FILE_SPEC should be in the format \'SRC -> DST\' where SRC is the source path to the file and DST is the full destination path on the VM drive, begining with a / character. NOTE: /tmp directories are sometimes cleared during the boot process so you are best off copying files to other directories if you want them to be available at the end of the boot process.',
        metavar='FILE_SPEC',
        multiple=True,
        converter=[parse_file_specs],
    ),
    mac_address = dict(
        flags=['-m', '--mac-address'],
        help_msg='Mac address to use on the VM\'s network interface. Will be randomly generated if not specified.',
        metavar='MAC_ADDRESS',
        converter=[gen_mac_if_missing],
    ),
    use_apt_proxy = dict(
        flags=['-p', '--apt-proxy'],
        help_msg='Proxy packages from the apt cache on the host if possible. Only available if the \'buildkit-apt-cache\' package is also installed',
        converter=[check_apt_proxy_available],
    ),
    exec_on_boot = dict(
        flags=['-e', '--exec-on-boot'],
        help_msg='A set of bash commands to be exectued at the end of the boot process, after files and directories have been copied',
        metavar='COMMANDS',
    ),
    #wait_for_boot = dict(
    #    flags=['--wait-for-boot'],
    #    help_msg='Don\'t exit until the system is booted and the login prompt is displayed',
    #),
    graphics = dict(
        flags=['--graphics'],
        help_msg='Also load a window for the VM. Note: If you do this, the start command won\'t return until the window is closed when the VM exits.',
    ),
    #console = dict(
    #    flags=['--console'],
    #    help_msg='Drop the user into a login prompt after boot',
    #),
)

def run(cmd):
    #if cmd.opts.wait_for_boot or cmd.opts.copy_dir:
    #    cmd.err('One of the options you\'ve chosen isn\'t implemented yet')
    #    return 1
    if os.geteuid() != 0:
        cmd.err("This script must be run as root")
        return 1
    extra = []
    for c in cmd.args[1:]:
        if c.strip() in ['-h', '--help']:
            cmd.err('ERROR: Help flags must be specified before the image name NAME')
            return 5
        else:
            extra.append(c)
    if cmd.args[0] in [instance.image for instance in get_vm_info()]:
        cmd.err('ERROR: The image %r is already in use', cmd.args[0])
        return 4
    # Make sure there isn't already a version of this image running
    if not cmd.opts.ip:
        cmd.err("No IP address available")
        return 3
    else:
        cmd.out("Host IP is %s", cmd.opts.ip)
    interface = determine_interface(cmd.opts.ip)
    if not interface:
        cmd.err("No network interface available")
        return 2
    else:
        cmd.out("Network interface is %s", interface)
    if cmd.opts.use_apt_proxy:
        start_apt_cacher_ng_if_not_running()
    bridge_info = get_bridge_info()
    add = True
    if cmd.opts.bridge_name in bridge_info.bridges.keys():
        add = False
    create_bridge(interface, cmd.opts.bridge_name, add=add)
    tunnel = cmd.opts.tunnel
    if tunnel is None:
        tunnel = gen_tunnel(cmd.opts.bridge_name)
    if add or tunnel not in bridge_info.bridges[cmd.opts.bridge_name]:
        create_tunnel(tunnel)
    path = "/var/lib/buildkit/vm/%s/vmtmp"%cmd.args[0]
    mount_image("/var/lib/buildkit/vm/%s/disk.raw"%cmd.args[0], path)
    update_image(cmd.args[0], cmd.opts.ip, use_apt_proxy=cmd.opts.use_apt_proxy)
    for spec in cmd.opts.copy_file:
        shutil.copy2(spec.src, os.path.join(path, spec.dst[1:]))
    if cmd.opts.exec_on_boot:
        fp = open(os.path.join(path, 'etc/buildkit_on_start.sh'), 'w')
        fp.write('#!/bin/sh\n\n')
        fp.write(cmd.opts.exec_on_boot)
        fp.close()
        os.chmod(os.path.join(path, 'etc/buildkit_on_start.sh'), stat.S_IEXEC)
    umount_image(path)
    opts = cmd.opts.copy()
    opts['tunnel'] = tunnel
    cmd.out("Starting VM "+cmd.args[0]+" on %(tunnel)s to %(bridge_name)s with MAC %(mac_address)s ..."%opts)
    def out(fh, stdin, output, exit):
        pass
    monitor = []
    serial = []
    def err(fh, stdin, output, exit):
        while not monitor or not serial:
            line = fh.readline()
            if line.startswith('char device redirected to '):
                device = line[len('char device redirected to '):-1]
                if monitor:
                    serial.append(device)
                else:
                    monitor.append(device)
            else:
                output.write(line)
            if monitor and serial:
                exit.append(10)
    if not cmd.opts.graphics:
        extra.append('-nographic')
    result = stacks.process(
        [
            '/usr/bin/kvm',
            '-enable-kvm',
            '-M', 'pc-0.12', 
            '-serial', 'pty',
            '-monitor', 'pty',
            #'-parallel', 'none',
            #'-usb'
            '-name', 'dev',
            # Memory and CPU
            '-m', cmd.opts.mem,
            '-smp', cmd.opts.cpus,
            # Drive options
            '-boot', 'c',
            '-drive', 'file=/var/lib/buildkit/vm/%s/disk.raw,if=ide,index=0,boot=on'%cmd.args[0],
            # Network options
            '-net', 'nic,macaddr=%s'%cmd.opts.mac_address,
            '-net', 'tap,ifname=%s,script=no,downscript=no'%tunnel,
        ] + extra,
        wait_for_retcode=False,
        out=out,
        err=err,
    )
    serial = serial[0]
    monitor = monitor[0]
    # Save the serial and monitor information
    fp = open('/var/lib/buildkit/vm/%s/vmtmp/vm.info'%cmd.args[0], 'w')
    fp.write('%s\n%s\n%s'%(result.pid, serial, monitor))
    fp.close()
    # Output some success messages
    cmd.out('Started successfully with pid %r'%result.pid)
    cmd.out('You can access the QEMU monitor for this VM like so:')
    cmd.out('    $ sudo screen %s', monitor)
    cmd.out('Once connected you should type \'Ctrl+a\' followed by \'k\' to leave the monitor. Typing \'quit\' will exit the VM.')
    if 0:# cmd.opts.console:
        os.system('screen %s'%serial)
    else:
        cmd.out('You can connect to the VM\'s serial console like this:')
        cmd.out('    $ sudo screen %s', serial)
        cmd.out('Again you can exit the console with \'Ctrl+a\' followed by \'k\'.')

