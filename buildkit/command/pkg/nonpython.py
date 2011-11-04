"""\
Package a non-Python library with an existing debian/control file
"""

import os
from buildkit import facilify
from buildkit.command.pkg import python

arg_specs = [
    dict(
        metavar='SRC_DIR',
        help_msg='the path to the package source to build from',
    ),
]
opt_specs_by_name = dict(
    force = dict(
        flags = ['-f', '--force'],
        help_msg = 'Overwrite any existing files and directories',
    ),
    deb = dict(
        flags=['--deb'],
        help_msg='generate a .deb file',
    ),
    rpm = dict(
        flags=['--rpm'],
        help_msg='generate an RPM file (implies --deb)',
    ),
    output_dir = dict(
        flags=['-o', '--output-dir'],
        help_msg='directory to place the generated .deb file',
        metavar='OUTPUT_DIR',
    ),
)
for name in [
    'packaging_version',
]:
    opt_specs_by_name[name] = python.opt_specs_by_name[name]

def run(cmd):
    count = 0
    for name in ['deb', 'rpm']:
        if cmd.opts[name]:
            count += 1
    if not count:
        cmd.err('ERROR: Expected at least one of --deb or --rpm')
        return 1
    if not os.path.exists(cmd.args[0]):
        cmd.err('ERROR: No such directory %r', cmd.args[0])
        return 1
    opts = facilify.str_keys(cmd.opts, ignore=['help'])
    if opts.has_key('output_dir'):
        opts['output_dir'] = facilify.uniform_path(opts['output_dir'])
    result = cmd.parent.dist.build_non_python(
        facilify.uniform_path(cmd.args[0]),
        **opts
    )
    if result.get('error'):
        cmd.err(result.error)
        return 1
    
