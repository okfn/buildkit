"""\
Manage the packages in a repository from testing through to release

Note: Packages are generated with the packaging license the same as the software license.
"""

import os
import platform
import shutil
import sys
import time
import types
import datetime
from buildkit import facilify
from buildkit.facility.build import get_pkg_info

def clone(
    repo, 
    repo_url, 
    destination_path, 
    revision='default',
):
    """\
    """
    repo_name = repo_url.split('/')[-1]
    repo_dir = destination_path
    revision = revision
    hgrc_filepath = os.path.join(repo_dir, '.hg', 'hgrc')
    msg = 'Get repo for "%s" source' % repo_name
    if os.path.exists(hgrc_filepath):
        repo.log.info(msg)
        facilify.process(
            'hg -R %(repo_dir)s pull'%dict(
                repo_url=repo_url, 
                repo_dir=repo_dir, 
                revision=revision,
            ),
            shell=True,
        )
        facilify.process(
            'hg -R %(repo_dir)s up -r %(revision)s'%dict(
                repo_url=repo_url, 
                repo_dir=repo_dir, 
                revision=revision,
            ),
            shell=True,
        )
    else:
        repo.log.info(msg)
        facilify.process(
            'hg clone %(repo_url)s -r %(revision)s %(repo_dir)s' % dict(
                 repo_url=repo_url,
                 repo_dir=repo_dir,
                 revision=revision
            ),
            shell=True,
        )
        assert os.path.exists(hgrc_filepath)

#
# Repo Helpers
#

def make_full_version_number(timestamp, changeset):
    return '%s~%s'%(timestamp, changeset.replace('-', '~'))

def existing_package_timestamp(packages_path, name, changeset):
    built, unbuilt, other_existing = do_packages_exist_already([(name, changeset)], packages_path)
    if unbuilt:
        return None
    else:
        return built[-1][1]

def do_packages_exist_already(deps, directory=None):
    """\
    ``directory``
        path to the directory containing the built packages
    ``deps``
        a list of dependencies where each dependency is specified in the form ``('python-ckanext-harvest', '0.2b1')``

    Returns:

    ``built``
        A list of the packages from the original dependencies that have already been built
    ``unbuilt``
        A list of the packages from the original dependencies that have not been built
    ``other_exising``
        Other packages, not in the list of original dependencies that happen to have been built anyway
    """
    unbuilt = deps[:]
    existing = os.listdir(directory)
    built = []
    other_existing = []
    for item in existing:
        if os.path.isdir(os.path.join(directory, item)):
            continue
        elif not item.endswith('.deb'):
            raise Exception('The path %r contains files which aren\'t .deb files such as %r'%(directory, item))
        parts = item.split('~')
        package = parts[0]
        full_version = '~'.join(parts[1:])
        parts = package.split('_')
        timestamp = parts[-1]
        package = '_'.join(parts[0:-1])
        changeset = full_version.split('+')[0]
        if not (package, changeset) in deps:
            if not (package, changeset) in other_existing:
                other_existing.append((package, timestamp, changeset))
        else:
            if not (package, changeset) in built:
                built.append((package, timestamp, changeset))
    for item in built:
        if (item[0], item[2]) in unbuilt:
            repo.log.info("  Package %r changeset %r is already built", item[0], item[2])
            unbuilt.pop(unbuilt.index((item[0], item[2])))
    built.sort()
    other_existing.sort()
    return built, unbuilt, other_existing

def get_dependencies(
    repo, 
    path,
    packages_dir,
    deps_rename,
    deps_delete,
):
    requires_missing = os.path.join(path, 'requires', 'lucid_missing.txt')
    if not os.path.exists(requires_missing):
        raise Exception('No such file %r'%(requires_missing,))
    repo.log.info('  Getting dependencies for %r ...', path)
    timestamp='5'
    present = repo.determine_dependencies_from_present_file(
        path,
        deps_rename=deps_rename,
        deps_delete=deps_delete,
    )
    present_deps = ', '.join(present)
    if present:
        repo.log.info('    Ubuntu Python dependencies are: %r', present_deps)
    # Look at the lucid_missing file to get python dependencies that need packaging
    missing, missing_requirements = repo.determine_dependencies_from_missing_file(
        path,
        deps_rename=deps_rename,
        deps_delete=deps_delete,
    )
    # @@@ Ignoring conflicts code for the moment, conflicts should be picked up when trying to import into a repository
    #for pkg_name, vers in missing:
    #    if conflicts.has_key(pkg_name) and conflicts[pkg_name][0] != vers:
    #        repo.log.error(
    #            'The %r instance requires %r changeset %r but the '
    #            '%r instance requires changeset %r. Continuing but '
    #            'the behaviour is undefined, it may cause serious '
    #            'problems. This error won\'t be shown again if you '
    #            're-run the script so please fix it now if it is a '
    #            'genuine issue',
    #            package_name,
    #            pkg_name, 
    #            vers,
    #            conflicts[pkg_name][1],
    #            conflicts[pkg_name][0],
    #        )
    #    else:
    #        conflicts[pkg_name] = (vers, repo_name)

    # See if these packages have already been built
    built = None
    unbuilt = None
    if packages_dir is not None:
        built, unbuilt, other_existing = do_packages_exist_already(
            missing, 
            directory=packages_dir,
        )
        result = []
        for m in built:
            result.append(
                "%s (>=%s~%s)"%(
                    m[0], 
                    m[1],
                    m[2],
                )
            )
        for m in unbuilt:
            result.append(
                "%s (>=%s~%s)"%(
                    m[0], 
                    timestamp,
                    m[1],
                )
            )
    missing_deps = ', '.join(result)
    if missing_deps:
        repo.log.info('    Non-Ubuntu Python dependencies are: %r', missing_deps)
    return facilify.obj(
        present_deps=present_deps, 
        missing_deps=missing_deps, 
        unbuilt=unbuilt,
        missing_requirements=missing_requirements,
    )

def parse_control_file(path):
    fp = open(path, 'r')
    content = fp.read().split('\n')
    fp.close()
    control = facilify.OrderedDict()
    for line in content:
        if line.strip() and not line.strip().startswith('#') and not line.startswith(' '):
            parts = line.strip().split(': ')
            key = parts[0]
            value = ': '.join(parts[1:])
            control[key] = value
    return control

def save_control_file(path, control, warn=True):
    if warn and os.path.exists(path):
        repo.log.warning('Overwriting the existing file at %r', path)
    fp = open(path, 'wb')
    control = fp.write('\n'.join(['%s: %s'%(k,v) for k,v in control.items()])+'\n')
    fp.close()

