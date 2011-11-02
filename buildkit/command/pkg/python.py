"""\
Package a Python library, generating the required DEBIAN/control file automatically
"""

import os
import tempfile
import shutil
from buildkit import facilify
from buildkit.command import start

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
    section = dict(
        flags = ['-s', '--section'],
        help_msg = 'The section of the distribution repository, defaults to \'main/python\'',
        default='main/python',
        metavar='SECTION',
    ),
    architecture = dict(
        flags = ['-a', '--architecture'],
        help_msg = 'The build architecture, defaults to \'all\'',
        default='all',
        metavar='ARCHITECTURE',
    ),
    packaging_version = dict(
        flags = ['-p', '--packaging-version'],
        metavar='PACKAGING_VERSION',
        default='01',
        help_msg=(
            'package version containing characters +~.0-9A-Za-z, often ~ is '
            'used to differentiate a particular build of a version eg '
            '`0.1.1~01\''
        ),
    ),
    debian_dir = dict(
        flags=['--debian-dir'],
        help_msg='generate a template debian directory in the output directory',
    ),
    no_package = dict(
        flags=['--no-package'],
        help_msg='don\'t actually build the package (usually only used with the --debian-dir option)',
    ),
    deb = dict(
        flags=['--deb'],
        help_msg='generate an .deb file',
    ),
    rpm = dict(
        flags=['--rpm'],
        help_msg='generate an RPM file (implies --deb)',
    ),
    install_missing_requirements = dict(
        flags=['--deps'],
        help_msg='also build all the dependencies',
    ),
    output_dir = dict(
        flags=['-o', '--output-dir'],
        help_msg='directory to place the generated .deb file',
        metavar='OUTPUT_DIR',
    ),
    deps_rename = dict(
        flags=['-e', '--rename'],
        help_msg='explictly define how a Python package name should be mapped to an existing Debian package name eg --rename "repoze.who.plugins.openid->repoze.who-plugins"; this doesn\'t work for packages we build ourselves; don\'t include the \'python-\' part, it will be added automatically',
        metavar='SPEC',
        multiple=True
    ),
    conflict_module = dict(
        flags=['--conflict-module'],
        help_msg='explictly define the name of a module within Python package to use as the conlict module eg --module "sqlalchemy-migrate -> migrate"',
        metavar='SPEC',
        multiple=True
    ),
    deps_delete = dict(
        flags=['--delete'],
        help_msg='don\'t include this Python dependency as a package, perhaps it is already met by the inclusion of another package"',
        metavar='SPEC',
        multiple=True
    ),
    license_file = dict(
        flags=['--license-file'],
        help_msg='path to a file containing a license (note: common ones are already in /usr/share/common-licenses)',
        metavar='LICENSE_FILE',
    ),
    #license_name = dict(
    #    flags=['--license-name'],
    #    help_msg='a short name for the license, eg GPL2, AGPL3, BSD etc',
    #    metavar='LICENSE_NAME',
    #),
    packager_name = dict(
        flags = ['--packager-name'],
        help_msg = 'Name of the person responsible for packaging the software',
        metavar='PACKAGER_NAME',
    ),
    packager_email = dict(
        flags = ['--packager-email'],
        help_msg = 'Contact email of the person given in `--packager-name\'',
        metavar='PACKAGER_EMAIL',
    ),
    build_dir = dict(
        flags=['-b', '--build-dir'],
        help_msg='where the generated project template should be created',
        metavar='BUILD_DIR',
    ),
    exclude = dict(
        flags=['-x', '--exclude'],
        help_msg='pattern relative to SRC_DIR of files to exclude, eg .git',
        metavar='RSYNC_PATTERN',
        multiple=True,
    ),
    no_rmtmpdir = dict(
        flags=['--skip-remove-tmp-dir'],
        help_msg='don\'t remove any tmp directory created, useful for debugging',
    ),
    no_present = dict(
        flags=['--no-present'],
        help_msg='don\'t include present packages as dependencies',
    ),
    no_missing = dict(
        flags=['--no-missing'],
        help_msg='don\'t package missing packages as dependencies',
    ),
)
for name in [
    'url', 
    'author_name',
    'author_email',
    'version',
    'distro_depends',
    'copyright_year',
]:
    opt_specs_by_name[name] = start.opt_specs_by_name[name].copy()
# We don't want a default value here
del opt_specs_by_name['version']['default']

def run(cmd):
    src_dir = cmd.args[0]
    ## Check for errors
    count = 0
    for name in ['deb', 'rpm', 'debian_dir']:
        if cmd.opts[name]:
            count += 1
    if not count:
        cmd.err('ERROR: Expected at least one of --deb, --rpm or debian_dir')
        return 1
    if not os.path.exists(src_dir):
        cmd.err('ERROR: No such directory %r', src_dir)
        return 1
    opts = facilify.str_keys(cmd.opts, ignore=['help', 'license_file'])
    if opts.no_package and opts.rpm:
        cmd.err('ERROR: You can\'t specify both --rpm and --no-package options together')
        return 1
    ## Prepare the options
    opts['license_text'] = ''
    if cmd.opts.license_file is not None:
        fp = open(cmd.opts.license_file, 'r')
        opts['license_text'] = fp.read()
        fp.close()
    # See if any pip requirements have changed
    conflict_modules = {}
    for dep in cmd.opts.conflict_module:
        k, v = dep.split('->')
        conflict_modules[k.strip()] = v.strip()
    opts['conflict_module'] = conflict_modules
    deps_rename = {}
    for dep in cmd.opts.deps_rename:
        k, v = dep.split('->')
        deps_rename[k.strip()] = v.strip()
    opts['deps_rename'] = deps_rename
    build_dir = os.path.join(src_dir, 'build')
    if not cmd.opts.output_dir:
        if not os.path.exists(os.path.join(src_dir, 'dist')):
            os.mkdir(os.path.join(src_dir, 'dist'))
        if not os.path.exists(os.path.join(src_dir, 'dist', 'buildkit')):
            os.mkdir(os.path.join(src_dir, 'dist', 'buildkit'))
        opts['output_dir'] = os.path.join(src_dir, 'dist', 'buildkit')
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)
    bk_build_dir = os.path.join(build_dir, 'buildkit')
    if not os.path.exists(bk_build_dir):
        os.mkdir(bk_build_dir)
    opts['build_env_dir'] = os.path.join(bk_build_dir, 'env')
    results = []
    build_python(cmd, opts, results)
    for result in results:
        if result.error:
            cmd.err(result.error)
            return 1
    cmd.out('Building took place in %r', opts['build_env_dir'])
    cmd.out('Packages were placed in %r', opts['output_dir'])

def build_python(cmd, opts, results):
    # Build the packages
    rm_build_dir = False
    if opts.build_dir is None:
        rm_build_dir = True
        opts['build_dir']=tempfile.mkdtemp()
    del opts['no_rmtmpdir']
    try:
        result = cmd.parent.dist.build_python(
            facilify.uniform_path(cmd.args[0]),
            **opts
        )
        results.append(result)
        if opts.install_missing_requirements:
            for key in [
                'author_name',
                'author_email',
                'install_missing_requirements',
                'distro_depends',
                'package',
                'version',
                'packaging_version',
                'url',
                'description',
                'exclude',
            ]:
                if opts.has_key(key):
                    del opts[key]
            opts['no_conflict'] = True
            for dep in result.calculated_deps.missing_requirements:
                package_name = dep[0]
                src_dir = os.path.join(opts.build_env_dir, 'src', package_name)
                result = cmd.parent.dist.build_python(
                    facilify.uniform_path(src_dir),
                    **opts
                )
                results.append(result)
    finally:
        if rm_build_dir:
            if cmd.opts.no_rmtmpdir:
                cmd.out('The tmp directory %r has been left', opts['build_dir'])
            else:
                shutil.rmtree(opts['build_dir'])
    
