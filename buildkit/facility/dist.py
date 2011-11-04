"""\
Manage the packages in a repository from testing through to release

Note: Packages are generated with the packaging license the same as the software license.
"""

import logging
import os
import platform
import shutil
import sys
import time
import types
import datetime
import pkg_resources
from wsgiref.handlers import _weekdayname, _monthname
from buildkit import facilify
from buildkit.facility.build import get_pkg_info

log = logging.getLogger(__name__)

def utcnow():
    year, month, day, hh, mm, ss, wd, y, z = time.gmtime(time.time())
    return "%s, %02d %3s %4d %02d:%02d:%02d +0000" % (
        _weekdayname[wd], day, _monthname[month], year, hh, mm, ss
    )

def parse_control_file(path):
    fp = open(path, 'r')
    content = fp.read().split('\n')
    fp.close()
    control = facilify.OrderedDict()
    key = None
    for line in content:
        if line.strip() and not line.strip().startswith('#') and not line.startswith(' '):
            parts = line.split(': ')
            key = parts[0].strip()
            value = ': '.join(parts[1:])
            control[key] = value
        elif key is not None:
            control[key] += '\n'
    return control

def save_control_file(path, control, warn=True):
    if warn and os.path.exists(path):
        log.warning('Overwriting the existing file at %r', path)
    items = []
    for key in [
        'Source',
        'Section',
        'Priority',
        'Maintainer',
        'Build-Depends',
        'Standards-Version',
        'XS-Python-Version',
        'Version',
        'Homepage',
    ]:
        if control.has_key(key):
            items.append((key, control[key]))
            del control[key]
    for k,v in control.items():
        items.append((k,v))
    fp = open(path, 'wb')
    control = fp.write('\n'.join(['%s: %s'%(k,v) for k,v in items])+'\n')
    fp.close()

def determine_distro(
    dist,
):
    fp = open('/etc/lsb-release', 'r')
    data = fp.read().split('\n')
    fp.close()
    for line in data:
        name, value = line.split('=')
        if name.strip() == 'DISTRIB_CODENAME':
            return value.strip()
    return None

def determine_arch(
    dist
):
    if platform.machine() == 'x86_64':
        return 'amd64'
    elif platform.machine() in ['i386', 'i486', 'i586', 'i686']:
        return 'i386'
    else:
        raise Exception('Unsupported machine %s, cannot determine the architecture'%platform.machine())

#
# Core functionality
#

def prepare_build_dir(
   dist,
   package, 
   full_version, 
   src_dir, 
   build_dir, 
   force=False,
   exclude=None
):
    if exclude is None:
        exclude=[]
    template_vars = dict(
        package=package, 
        full_version=full_version, 
        src_dir=src_dir,
        build_dir=build_dir,
        exclude=' --exclude='.join(exclude),
    )
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)
    output_dir = os.path.join(build_dir, 'python-%s-%s'%(package, full_version))
    if os.path.exists(output_dir):
        if force:
            shutil.rmtree(output_dir)
        else:
            raise Exception('The output directory %r already exists and force is set to False, not overwriting'%output_dir)
    if not os.path.exists(src_dir):
        raise Exception('No such source directory %r'%src_dir)
    elif not os.path.exists(os.path.join(src_dir, package.split('.')[0])):
        raise Exception('No such package directory %r in %r, is your package name correct?'%(package.split('.')[0], src_dir))
    cmd = ("""
        mkdir %(build_dir)s/%(package)s-%(full_version)s/
        rsync -aHxv --progress --exclude=*.swp --exclude=*.pyc --exclude=build --exclude=dist --exclude=.git --exclude=.gitignore --exclude=.hg --exclude=.hgtags --exclude=.hgignore --numeric-ids %(exclude)s ./ %(build_dir)s/%(package)s-%(full_version)s/
        ls %(build_dir)s/%(package)s-%(full_version)s/
        cd %(build_dir)s
        tar -cvzf %(build_dir)s/%(package)s-%(full_version)s.tar.gz %(package)s-%(full_version)s
        mv %(package)s-%(full_version)s python-%(package)s-%(full_version)s
    """%template_vars)
    #log.info(cmd)
    result = facilify.process(
        cmd,
        shell=True,
        cwd=src_dir,
        merge=True,
    )
    #log.info(result.stdout)
    return result

def make_debian_dir(
   dist,
   package, 
   full_version, 
   build_dir,
   packager_name,
   packager_email,
   force=False,
   exclude=None
):
    if exclude is None:
        exclude=[]
    template_vars = dict(
        packager_name=packager_name,
        packager_email=packager_email,
        package=package, 
        full_version=full_version, 
        build_dir=build_dir,
        exclude=' --exclude='.join(exclude),
    )
    cmd = ''
    if packager_name is not None:
        cmd += ('export DEBFULLNAME="%(packager_name)s"\n'%template_vars)
    if packager_email is not None:
        cmd += ('export DEBEMAIL="%(packager_email)s"\n'%template_vars)
    cmd += ("""
        cd python-%(package)s-%(full_version)s
        echo "\n" | dh_make  -s -b -f "../%(package)s-%(full_version)s.tar.gz"
        cd debian
        rm *ex *EX
        rm README.Debian
        rm README.source
    """%template_vars)
    #log.info(cmd)
    result = facilify.process(
        cmd,
        shell=True,
        cwd=build_dir,
        merge=True,
    )
    #log.info(result.stdout)
    return result

def update_copyright(
    dist,
    build_dir, 
    package, 
    full_version, 
    url, 
    author_name,
    author_email,
    license_text,
    copyright_year,
):
    fp = open(os.path.join(build_dir, "python-%s-%s"%(package, full_version), 'debian', 'copyright'), 'r')
    data = fp.read()
    fp.close()
    data = data.replace(
        "<Put the license of the package here indented by 4 spaces>\n",
        '\n    '.join(license_text.split('\n'))+'\n',
    )
    data = data.replace(
        "It was downloaded from <url://example.com>",
        "It was downloaded from <%s>"%url,
    )
    data = data.replace(
        "    <put author's name and email here>\n    <likewise for another author>",
        "    %s <%s>"%(author_name, author_email),
    )
    data = data.replace(
        "    <Copyright (C) YYYY Name OfAuthor>\n    <likewise for another author>",
        "    Copyright (C) %s %s <%s>"%(copyright_year, author_name, author_email),
    )
    data = data.replace(
"""\

# Please chose a license for your packaging work. If the program you package
# uses a mainstream license, using the same license is the safest choice.
# Please avoid to pick license terms that are more restrictive than the
# packaged work, as it may make Debian's contributions unacceptable upstream.
# If you just want it to be GPL version 3, leave the following lines in.

and is licensed under the GPL version 3, 
see `/usr/share/common-licenses/GPL-3'.

# Please also look if there are files or directories which have a
# different copyright/license attached and list them here.""",
    "\nand is licensed under the same license specified above."
    )
    fp = open(os.path.join(build_dir, "python-%s-%s"%(package, full_version), 'debian', 'copyright'), 'w')
    fp.write(data)
    fp.close()

def create_control_template(
    dist,
    build_dir, 
    package, 
    full_version, 
    url, 
    author_name,
    author_email,
    section='main/python', 
    distro_depends=None, 
    description=None,
    architecture='all',
):
    if architecture != 'all':
        if platform.machine() == 'x86_64' and architecture != 'amd64':
            raise Exception("Only architectures 'all' and 'amd64' are supported on this x86_64 machine")
        elif platform.machine() == 'x86' and architecture != 'i386':
            raise Exception("Only architectures 'all' and 'i386' are supported on this x86 machine")
    if distro_depends is None:
        distro_depends = []
    control = parse_control_file(os.path.join(build_dir, "python-%s-%s"%(package, full_version), 'debian', 'control'))
    control['Section'] = section
    control['Maintainer'] = "%(author_name)s <%(author_email)s>"%dict(
        author_name=author_name, 
        author_email=author_email,
    )
    control['Homepage'] = url+'\n'
    control['Build-Depends'] = 'cdbs (>= 0.4.49), debhelper (>= 7), python (>= 2.5), python-support'
    control['Depends'] = '${misc:Depends}, ${python:Depends}'
    control['XS-Python-Version'] =  '>= 2.5'
    control['Architecture'] = architecture
    for dep in distro_depends:
        control['Depends'] += ', '+dep
    if description is None:
        control['Description'] = package[:60]+'\n'
    else:
        control['Description'] = description+'\n'
    #control = list(control.items())
    #control.insert(5, ('XS-Python-Version', '>= 2.5'))
    #control.insert(-2, ('Recommends', ''))
    save_control_file(
        os.path.join(
            build_dir, 
            "python-%s-%s"%(package, full_version), 
            'debian', 
            'control.template',
        ),
        control, 
        warn=False,
    )

def update_rules(
    dist,
    build_dir, 
    package,
    full_version,
):
    fp = open(os.path.join(build_dir, "python-%s-%s"%(package, full_version), 'debian', 'rules'), 'wb')
    control = fp.write("""\
#!/usr/bin/make -f

DEB_PYTHON_SYSTEM=pysupport

include /usr/share/cdbs/1/rules/debhelper.mk
include /usr/share/cdbs/1/class/python-distutils.mk""")
    fp.close()

def update_changelog(
    dist,
    build_dir, 
    package, 
    full_version,
    author_name,
    author_email,
):
    text = """\
python-%s (%s-1) lucid; urgency=low

  * Automatically generated package

 -- %s <%s>  %s
"""	%(
        package, 
        full_version,
        author_name,
        author_email,
        #Thu, 09 Jun 2011 14:10:11 +0100
        utcnow(),
    )
    fp = open(os.path.join(build_dir, "python-%s-%s"%(package, full_version), 'debian', 'changelog'), 'wb')
    fp.write(text)
    fp.close()

def build_package(
    dist,
    build_dir, 
    package, 
    full_version, 
):
    return facilify.process(
        """
        export DEBFULLNAME="James Gardner"
        export DEBEMAIL="james.gardner@okfn.org"
        debuild -us -uc
        """, 
        shell=True,
        cwd=os.path.join(build_dir, "python-%s-%s"%(package, full_version)),# 'debian', 'rules'), 'wb')
        merge=True,
    )

def output_debian_dir_template(
    dist,
    build_dir,
    debian_dir,
    package,
    full_version,
):
    shutil.copytree(
        os.path.join(build_dir, "python-%s-%s"%(package, full_version), 'debian'),
        debian_dir,
    )

def copy_debian_dir(
    dist,
    debian_path,
    full_version, 
    build_dir, 
    package, 
):
    shutil.copytree(
        debian_path,
        os.path.join(build_dir, "python-%s-%s"%(package, full_version), 'debian'),
    )

def control_from_template(
    dist,
    debian_path,
    full_version=None, 
    deps=None,
):
    # We need to parse the template, add any missing dependencies, then add more variables
    control_path = os.path.join(
        debian_path,
        'control',
    )
    # Get the current dependencies from the control template file.
    control = parse_control_file(control_path+'.template')
    # Update the dependencies with missing and present values
    if deps is not None:
        control['Depends'] = ((', '.join([control['Depends'], deps]))).strip()
        while ', ,' in control['Depends']:
            control['Depends'] = control['Depends'].replace(', ,', ',')
        if control['Depends'].endswith(','):
            control['Depends'] = control['Depends'][:-1]
    if full_version is not None:
        control['Version'] = full_version
    # Save the change
    save_control_file(control_path, control, warn=False)
    
def copy_package(
    dist,
    build_dir, 
    package, 
    full_version, 
    output_dir=None,
    architecture='all',
):
    if output_dir is None:
        output_dir = os.getcwd()
    src = os.path.join(build_dir, "python-%s_%s-1_%s.deb"%(package, full_version, architecture))
    dst = os.path.join(output_dir, "python-%s_%s-1_%s.deb"%(package, full_version, architecture))
    error = None
    try:
        os.rename(src, dst)
    except OSError, e:
        try:
            shutil.copyfile(src, dst)
        except OSError, e:
            error = ' Failed: Could not copy %r to %r: %s' %(src, dst, e)
    return facilify.obj(error=error, dst=dst)

def deps(
    dist, 
    src_dir,
    build_env_dir,
    build_src_dir,
    deps_rename,
    deps_delete,
    package,
    install_missing_requirements=False,
    conflict_module=None,
    no_conflict=False,
    no_present=False,
    no_missing=False,
):
    dist.log.info('  Building python-%s ...', src_dir.split('/')[-1])
    dist.log.info('    Analysing dependencies in requires/* files ...')
    present_error = missing_error = None
    present_deps = missing_deps = conflict_deps = ''
    missing_requirements = conflict_requirements = {}
    requires_present = os.path.join(src_dir, 'requires', 'lucid_present.txt')
    if not os.path.exists(requires_present):
        present_error='No such file %r'%(requires_present,)
    elif not no_present:
        result = dist.parse_deps(
            src_dir=src_dir,
            build_env_dir=build_env_dir,
            deps_rename=deps_rename,
            deps_delete=deps_delete,
            rel_requires_path='requires/lucid_present.txt',
        )
        for dep in result.distro:
            # We don't need the version number for the present case
            present_deps += ', python-%s'%(dep[0],)
        if present_deps:
            # Strip the leading ", "
            present_deps = present_deps[2:]
            dist.log.info('    Ubuntu Python dependencies are: %r', present_deps)
    requires_missing = os.path.join(src_dir, 'requires', 'lucid_missing.txt')
    if not os.path.exists(requires_missing):
        missing_error = 'No such file %r'%(requires_missing,)
    elif not no_missing:
        result = dist.parse_deps(
            src_dir=src_dir,
            build_env_dir=build_env_dir,
            deps_rename=deps_rename,
            deps_delete=deps_delete,
            rel_requires_path='requires/lucid_missing.txt',
            install_requirements=install_missing_requirements,
        )
        missing, missing_requirements = result.distro, result.pip
        for dep in result.distro:
            missing_deps += ', python-%s (>=%s)'%(dep[0], dep[1].split('+')[0])
            #missing_deps += ', python-%s (>=%s), python-%s (<=%s)'%(dep[0], dep[1], dep[0], dep[1])
        if missing_deps:
            # Strip the leading ", "
            missing_deps = missing_deps[2:]
            dist.log.info('    Non-Ubuntu Python dependencies are: %r', missing_deps)
    requires_conflict = os.path.join(src_dir, 'requires', 'lucid_conflict.txt')
    if not os.path.exists(requires_conflict):
        conflict_error='No such file %r'%(requires_conflict,)
    elif not no_conflict:
        result = dist.parse_deps(
            src_dir=src_dir,
            build_env_dir=build_env_dir,
            deps_rename=deps_rename,
            deps_delete=deps_delete,
            rel_requires_path='requires/lucid_conflict.txt',
            install_requirements=True,
        )
        conflict, conflict_requirements = result.distro, result.pip
        for dep in result.distro:
            conflict_deps += ', python-%s (>=%s)'%(dep[0], dep[1].split('+')[0])
            #conflict_deps += ', python-%s (>=%s), python-%s (<=%s)'%(dep[0], dep[1], dep[0], dep[1])
        if conflict_deps:
            # Strip the leading ", "
            conflict_deps = conflict_deps[2:]
            dist.log.info('    Conflicting Python dependencies to be copied into the src distribution are: %r', conflict_deps)
        for dep in result.distro:
            package_name = dep[0]
            module_name = package_name
            if conflict_module and conflict_module.has_key(package_name):
                module_name = conflict_module[package_name]
            src = os.path.join(build_env_dir, "src", package_name, module_name)
            dst = os.path.join(build_src_dir, package, module_name.split('/')[-1])
            if not os.path.exists(src):
                raise Exception('Cannot copy conflicting package into src tree, the directory %r does not exist. Do you need to specify conflict_module?'%src)
            if os.path.exists(dst):
                raise Exception('Cannot copy conflicting package into src tree, the directory %r already exists'%dst)
            shutil.copytree(
                src,
                dst,
            )
    return facilify.obj(
        present_error=present_error,
        missing_error=missing_error,
        present_deps=present_deps, 
        missing_deps=missing_deps, 
        missing_requirements=missing_requirements,
        conflict_deps=conflict_deps,
        conflict_requirements=conflict_requirements,
    )

def parse_deps(
    dist, 
    src_dir, 
    build_env_dir,
    deps_rename, 
    deps_delete,
    rel_requires_path,
    install_requirements=False,
):
    error = None
    distro = []
    pip = {}
    pip_path = os.path.join(build_env_dir, 'bin', 'pip')
    if not os.path.exists(pip_path):
        result = facilify.process(['virtualenv', build_env_dir], merge=True)
        if result.retcode:
            dist.log.error(result.stdout)
            raise Exception('Failed to create a virtual environment in %r'%build_env_dir)
        result = facilify.process(
            [
                pip_path,
                'install',
                '--upgrade',
                'pip>=1.0,<=1.0.99',
            ],
            merge=True
        )
        if result.retcode:
            dist.log.error(result.stdout)
            raise Exception('Failed to upgrade pip %r'%pip_path)
    cache_path = os.path.join(build_env_dir, 'cache')
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)
    if os.path.exists(os.path.join(src_dir, rel_requires_path)):
        for line in facilify.file_contents(os.path.join(src_dir, rel_requires_path)).split('\n'):
            if not line.strip() or line.strip().startswith('#'):
                continue
            if line.strip().startswith('-e'):
                # This is an editable requirement
                requirement = line.strip()[2:].strip()
                cmd_ = [
                    pip_path, 
                    'install', 
                    # '--upgrade', 
                    '--no-deps', 
                    '--download-cache', cache_path,
                    '--ignore-installed', 
                    '-e', requirement,
                ]
                result = facilify.process(
                    cmd_,
                    merge=True,
                )
                if result.retcode:
                    dist.log.error(' '.join(cmd_))
                    dist.log.error(result.stdout)
                    raise Exception('Failed to create install requirement %r'%requirement)
                after_changeset = requirement.split('@')
                if not len(after_changeset)>1:
                    raise Exception('The changeset isn\'t specified in requirement %r'%requirement)
                else:
                    changeset, egg = after_changeset[-1].split('#egg=')
                if '.' in changeset:
                    dist.log.warning(
                        'The changeset part %r of requirement %r appears to be a version or a revision, not a revision ID',
                        changeset, 
                        requirement,
                    )
                parsed_data = get_pkg_info(os.path.join(build_env_dir, 'src', egg))
                version = parsed_data['Version'][0]+('+%s'%changeset)
                # Let's use the egg name, not the package name
                package = line.split('egg=')[-1].lower().strip().lower()
                if package in deps_delete:
                    continue
                if package in deps_rename.keys():
                    package  = deps_rename[package]
                #else:
                #    package = 'python-%s'%package
                tup = (package, version)
                distro.append(tup)
                pip[tup] = requirement
            else:
                # Assume it is a usual requirement
                requirement = line.strip()
                req = [x for x in pkg_resources.parse_requirements(requirement)][0]
                specs = req.specs
                if not len(specs) or not len(specs[0]):
                    raise Exception('Invalid requirement %r'%requirement)
                if not specs[0][0] == '==':
                    raise Exception("Only requierments using '==' are allowed, not %r"%(line.strip(),))
                version = specs[0][1]
                package = req.project_name.lower()
                if install_requirements:
                    src = os.path.join(build_env_dir, 'build', req.project_name)
                    dst = os.path.join(build_env_dir, 'src', package)
                    if not os.path.exists(os.path.join(build_env_dir, 'src')):
                        os.mkdir(os.path.join(build_env_dir, 'src'))
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    if os.path.exists(src):
                        shutil.rmtree(src)
                    cmd_ = [
                            pip_path, 
                            'install',
                            # '--upgrade',
                            '--no-deps', 
                            '--download-cache', cache_path,
                            '--ignore-installed', 
                            '--no-install',
                            requirement,
                        ]
                    dist.log.info(' '.join(cmd_))
                    result = facilify.process(
                        cmd_,
                        merge=True,
                    )
                    dist.log.info(result.stdout)
                    if result.retcode:
                        raise Exception('Failed to create install requirement %r'%requirement)
                    try:
                        os.rename(src, dst)
                    except Exception, e:
                        #import pdb; pdb.set_trace()
                        raise
                if package in deps_delete:
                    continue
                if package in deps_rename.keys():
                    package = deps_rename[package]
                #else:
                #    package = 'python-%s'%package
                tup = (package, version)
                distro.append(tup)
                pip[tup] = requirement
    else:
        error = 'No such file %r'%(os.path.join(path, rel_requires_path))
    return facilify.obj(
        distro=distro,
        pip=pip,
        error=error,
    )

def build_python(
    dist,
    src_dir,
    build_dir,
    build_env_dir,
    copyright_year,
    license_text,
    output_dir=None,
    section='main/python',
    architecture='all',
    deps_rename=None,
    deps_delete=None,
    packager_name=None,
    packager_email=None,
    force=False,
    no_package=False,
    debian_dir=None,
    rpm=False,
    deb=False,
    no_present=False,
    no_missing=False,
    conflict_module=None,
    # These are ignored when handling deps
    no_conflict=False,
    author_name=None,
    author_email=None,
    install_missing_requirements=False,
    distro_depends=None,
    package=None,
    version=None,
    packaging_version='01',
    url=None,
    description=None,
    exclude=None,
):
    if output_dir is None:
        output_dir = os.path.join(src_dir, 'dist')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if rpm:
        deb = True
    build_dir = facilify.uniform_path(build_dir)
    if distro_depends is None:
        distro_depends = []
    metadata = facilify.obj(
        description=description,
        author_name=author_name,
        author_email=author_email,
        version=version, 
        url=url, 
        package=package,
        #license_name='',
    )
    parsed_data = None
    for name, value in metadata.iteritems():
        if value is None:
            if parsed_data is None:
                parsed_data = get_pkg_info(src_dir)
                #['Status', 'Name', 'License', 'Author', 'Metadata-Version', 
                # 'Home-page', 'Summary', 'Platform', 'Version', 'Classifier',
                # 'Author-email', 'Description']
            if name == 'author_name':
                metadata[name] = parsed_data['Author'][0]
            elif name == 'package':
                metadata[name] = parsed_data['Name'][0].lower()
            elif name == 'description':
                metadata[name] = parsed_data['Summary'][0]
            elif name == 'url':
                metadata[name] = parsed_data['Home-page'][0]
            #elif name == 'license_name':
            #    metadata[name] = parsed_data['License'][0].split('\n')[0]
            else:
                metadata[name] = parsed_data[name.capitalize().replace('_', '-')][0]
    for k, v in metadata.items():
        if not v or v == 'UNKNOWN':
            #if k == 'author_email' and author_email is not None:
            #    metadata['author_email'] = author_email
            #elif k == 'packager_email' and packager_email is not None:
            #    metadata['packager_email'] = packager_email
            #elif k == 'author_name' and author_name is not None:
            #    metadata['author_name'] = author_name
            #elif k == 'packager_name' and packager_name is not None:
            #    metadata['packager_name'] = packager_name
            #elif k == 'url' and url is not None:
            #    metadata['url'] = url
            #else:
            return facilify.obj(error='No %s could be determined for the package, please specify it manually'%k)
    if not license_text:
        if os.path.exists(os.path.join(src_dir, 'LICENSE.txt')):
            fp = open(os.path.join(src_dir, 'LICENSE.txt'), 'r')
            license_text = fp.read().strip()
            fp.close()
    if not license_text:
        dist.log.warning('No license text could be determined for %r'%metadata.package)
        license_text = 'No license text could be determined when building the package. Please see the project website for license information.'
    full_version = '%s+%s+%s'%(metadata['version'], packaging_version, dist.determine_distro())
    result = dist.prepare_build_dir(
        full_version=full_version, 
        src_dir=src_dir,
        build_dir=build_dir, 
        force=force,
        package=metadata.package, 
        exclude=exclude,
    )
    if result.retcode:
        raise Exception('Failed to prepare the build dir')
    debian_path = os.path.join(src_dir, 'distro', 'lucid', 'debian')
    if os.path.exists(debian_path):
        result = dist.copy_debian_dir(
            debian_path=debian_path,
            full_version=full_version, 
            build_dir=build_dir, 
            package=metadata.package, 
            deps=deps,
        )
        if result.retcode:
            raise Exception('Failed to copy the debian package dir')
    else:
        result = dist.make_debian_dir(
            full_version=full_version, 
            build_dir=build_dir, 
            force=force,
            package=metadata.package, 
            packager_name=packager_name,
            packager_email=packager_email,
        )
        if result.retcode:
            raise Exception('Failed to generate the debian package dir')
        dist.create_control_template(
            build_dir=build_dir, 
            full_version=full_version, 
            section=section,
            architecture=architecture,
            distro_depends=distro_depends,
            package=metadata.package, 
            url=metadata.url,
            description=metadata.description,
            author_name=metadata.author_name,
            author_email=metadata.author_email,
        )
    build_src_dir = os.path.join(build_dir, 'python-%s-%s'%(metadata.package, full_version))
    # At this point we can parse the dependencies
    calculated_deps = dist.deps(
        src_dir,
        build_env_dir,
        build_src_dir=build_src_dir,
        deps_rename=deps_rename,
        deps_delete=deps_delete,
        install_missing_requirements=install_missing_requirements,
        no_conflict=no_conflict,
        no_missing=no_missing,
        no_present=no_present,
        package=metadata.package,
        conflict_module=conflict_module,
    )
    if calculated_deps.present_error:
        dist.log.warning(calculated_deps.present_error)
    if calculated_deps.missing_error:
        dist.log.warning(calculated_deps.missing_error)
    deps = ''
    if not no_present and calculated_deps.present_deps:
        deps = calculated_deps.present_deps
    if not no_missing:
        if deps:
            deps += ', '+calculated_deps.missing_deps
        else:
            deps = calculated_deps.missing_deps
    dist.log.info('  Fetching and analysing deps for %r ...', metadata.package)
    dist.control_from_template(
        # What about renaming?
        debian_path=os.path.join(build_src_dir, 'debian'),
        full_version=full_version, 
        deps=deps,
    )
    dist.update_copyright(
        build_dir=build_dir, 
        full_version=full_version, 
        package=metadata.package, 
        url=metadata.url,
        #description=metadata.description,
        author_name=metadata.author_name,
        author_email=metadata.author_email,
        license_text=license_text,
        copyright_year=copyright_year,
    )
    result = dist.update_rules(
        build_dir=build_dir, 
        full_version=full_version,
        package=metadata.package,
    )
    result = dist.update_changelog(
        build_dir=build_dir, 
        package=metadata.package, 
        full_version=full_version,
        author_name=metadata.author_name,
        author_email=metadata.author_email,
    )
    if debian_dir:
        dist.output_debian_dir_template(
            build_dir, 
            os.path.join(output_dir, '%s_%s_debian'%(metadata.package, full_version)),
            package=metadata.package, 
            full_version=full_version,
        )
    if no_package:
        this_result = facilify.obj(dst=None, error=None)
    else:
        build_result = dist.build_package(
            build_dir=build_dir,
            package=metadata.package, 
            full_version=full_version,
        )
        if build_result.retcode:
            dist.log.error(build_result.stdout)
            raise Exception('Failed to build the Debian package')
        build_result.update(
            dist.copy_package(
                build_dir=build_dir, 
                package=metadata.package,
                full_version=full_version,
                architecture=architecture,
                output_dir=output_dir,
            )
        )
        if rpm:
            facilify.process(['alien', '-r', build_result.dst])
        this_result = build_result
    this_result['calculated_deps'] = calculated_deps
    return this_result

def build_non_python(
    dist,
    src_dir,
    output_dir=None,
    packaging_version='01',
    force=False,
    rpm=False,
    deb=False,
):
    if output_dir is None:
        output_dir = os.getcwd()
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if rpm:
        deb = True
    if not os.path.exists(os.path.join(src_dir, 'DEBIAN')):
        raise Exception('No DEBIAN directory found in %r'%src_dir) 
    dist.log.info("Building the %s package"%src_dir)
    if os.path.exists(os.path.join(src_dir, 'DEBIAN', 'control.template')):
        full_version = '%s+%s+lucid'%(
            get_pkg_info(os.path.join(src_dir, '..'))['Version'][0],
            packaging_version,
        )
        dist.control_from_template(
            debian_path=os.path.join(src_dir, 'DEBIAN'),
            full_version=full_version,
        )
    cmd = [
        "dpkg-deb",
        "-b", 
        ".",
        output_dir,
    ]
    build_result = facilify.process(
        cmd,
        cwd = src_dir,
        merge = True,
    )
    if build_result.retcode:
        dist.log.error(build_result.stdout)
        build_result['error'] = 'Failed to build the Debian package'
    if rpm:
        control = parse_control_file(os.path.join(src_dir, 'DEBIAN', 'control'))
        cmd = [
            'alien', 
            '-r', os.path.join(
                output_dir, 
                '%s_%s_%s.deb'%(
                    control['Package'], 
                    control['Version'], 
                    control['Architecture'],
                ), 
            )
        ]
        result = facilify.process(
            cmd,
            cwd = output_dir,
            merge = True,
        )
    dist.log.info('Building non-Python package complete.')
    return build_result

