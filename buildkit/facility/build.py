import os
import sys
import logging

log = logging.getLogger(__name__)

from buildkit import facilify

#from subprocess import Popen, PIPE, STDOUT

#
# Helpers
#

#def run(cmd, echo_stdout=False, echo_stderr=False, merge=True, cwd=None, no_return=False, **popen_args):
#    """\
#    Execute a command given by the list of parts ``cmd`` in the directory
#    ``cwd``.
#    """
#    if merge:
#        stderr = STDOUT
#    else:
#        stderr = PIPE
#    if cwd is None:
#        process = Popen(cmd, stdout=PIPE, stderr=stderr, **popen_args)
#    else:
#        if not os.path.exists(cwd):
#            raise Exception('No such file or directory %r'%cwd)
#        process = Popen(cmd, stdout=PIPE, stderr=stderr, cwd=cwd, **popen_args)
#    stdout, stderr = process.communicate()
#    if echo_stdout:
#        print stdout
#    if echo_stderr:
#        print stderr
#    retval = process.wait()
#    if retval != 0:
#        raise Exception('Command %s failed with code %r. Output: %s, %s'%(' '.join(cmd), retval, stdout, stderr))
#    if not no_return:
#        if merge:
#            return retval, stdout
#        else:
#            return retval, stdout, stderr

def cp(src, dst):
    """\
    Copy a file from ``src`` to ``dst``
    """
    src_fp = open(src, 'rb')
    dst_fp = open(dst, 'wb')
    dst_fp.write(src_fp.read())
    dst_fp.close()
    src_fp.close()

#
# Basic commands
#

def remove_dist(path):
    """\
    Remove the ``build`` and ``dist`` directories from the package whose
    package root is at ``path``.
    """
    dist_path = facilify.uniform_path(os.path.join(path, 'dist'))
    build_path = facilify.uniform_path(os.path.join(path, 'build'))
    if os.path.exists(dist_path):
        log.debug("Removing %s"%dist_path)
        run(['rm', '-r', dist_path])
    if os.path.exists(build_path):
        log.debug("Removing %s"%build_path)
        run(['rm', '-r', build_path])

def status(path):
    run(['hg', 'st'], cwd=facilify.uniform_path(path))

def update(path):
    run(['hg', 'update'], cwd=path)

def pull(path):
    """XXX pexpect needed??"""
    run(['hg', 'pull'], cwd=facilify.uniform_path(path))

def build_dist(
    path,
    third_party_eggs_path,
    python='python2.6',
    setuptools_version='setuptools-0.6c11-py2.6.egg',
):
    if os.path.exists(path):
        if not os.path.exists(
            os.path.join(path, setuptools_version) 
        ):
            log.debug(
                "Copying %s to %r"%(
                    os.path.join(third_party_eggs_path, setuptools_version), 
                    path
                )
            )
            cp(
                os.path.join(third_party_eggs_path, setuptools_version), 
                os.path.join(path, setuptools_version)
            )
        log.debug("Building in %s"%path)
        run([python, 'setup.py', 'sdist'], cwd=path)
    else:
        raise Exception('No such path %r'%path)

def scan_for_files(base_path, ext=None):
    found = []
    for dirpath, dirname, filenames in os.walk(base_path):
        for filename in filenames:
            if ext is None or filename.lower().endswith('.'+ext):
                found.append(facilify.uniform_path(os.path.join(dirpath, filename)))
    return found

def copy_files_to(found, dst):
    for path in found:
        if not path == dst:
            src_filename = facilify.uniform_path(path).split('/')[-1]
            dst_filename = os.path.join(dst, src_filename)
            log.debug("Copying %s to %s"%(path, dst_filename))
            cp(path, dst_filename)

def prepare_sources(src, dst):
    copy_files_to(scan_for_files(src, 'tar.gz'), dst)

def test_dist(
    requirement, 
    path, 
    eggs_path, 
    third_party_eggs_path,
    python='python2.6',
    test_requirement=None,
):
    """
    name
        The name of the package (ie its requiement)
    path
        The path to the source dir
    source
        The path conating the virtualenv file and setuptools egg
    third_party_eggs_path
        The path to other eggs
    """
    test_path = os.path.join(path, 'dist')
    if not os.path.exists(test_path):
        raise Exception('No test path %s'%test_path)
    log.debug("Creating virtual environment in %s"%test_path)
    run(
        [
            python, 
            os.path.join(third_party_eggs_path, 'virtualenv.py'), 
            'env'
        ],
        cwd=test_path
    )
    log.debug("Installing eggs")
    run(
        [
            'env/bin/easy_install', 
            '-f', "%s %s %s"%(
                '.',
                eggs_path.replace(' ', '\\ '), 
                third_party_eggs_path.replace(' ', '\\ '), 
            ),
            '--allow-hosts', '--None--',
            requirement,
        ],
        cwd=test_path
    )
    if test_requirement is not None:
        run(
            [
                'env/bin/easy_install', 
                '-f', "%s %s %s"%(
                    eggs_path.replace(' ', '\\ '), 
                    third_party_eggs_path.replace(' ', '\\ '),
                    '.',
                ),
                '--allow-hosts', '--None--',
                test_requirement,
            ],
            cwd=test_path
        )
    log.debug("Extracting source")
    cur_file = ''
    for file in os.listdir(test_path):
        if file.endswith('.tar.gz'):
            if file > cur_file:
                cur_file = file
    if not cur_file:
        log.debug('Could not find the distribution file')
        return 2, stdout
    else:
        run(['tar', 'zxfv', cur_file], cwd=test_path)
        cwd = os.path.join(test_path, cur_file[:-len('.tar.gz')], 'test')
        log.debug("Running tests in %r"%cwd)
        retval, stdout = run(
            [
                '../env/bin/python', 
                'setup.py',
                'develop',
            ], 
            cwd=os.path.join(test_path, cur_file[:-len('.tar.gz')])
        )
        retval, stdout = run(
            [
                '../../env/bin/python', 
                'doc.py',
            ], 
            cwd=cwd,
        )
        if '***Test Failed***' in stdout:
            return 1, stdout
        else:
            return 0, stdout

def egg_info(pyenv, name):
    return run(
        [
            os.path.join(pyenv, 'bin', 'python'),
            'setup.py',
            'egg_info',
        ], 
        cwd=os.path.join(pyenv, 'src', name),
        echo_stdout=True
    )

#
# Compound handlers
#


def handle_one(
    path,
    requirement,
    eggs_path,
    third_party_eggs_path,
    python='python2.6',
    setuptools_version='setuptools-0.6c11-py2.6.egg',
    test_requirement=None,
):
    remove_dist(path)
    build_dist(
        path,
        third_party_eggs_path=third_party_eggs_path,
        python=python,
        setuptools_version=setuptools_version,
    )
    test_dist(
        requirement,
        path, 
        eggs_path=eggs_path,
        third_party_eggs_path=third_party_eggs_path,
        python=python, 
        test_requirement=requirement,
    )

#
# Documentation Handlers
#

def get_pkg_info(path):
    # Cope with capitalisation variations
    facilify.process(['python', 'setup.py', 'egg_info'], cwd=path)
    files = os.listdir(path)
    name = None
    for filename in files:
        if os.path.isdir(os.path.join(path, filename)) and filename.endswith('.egg-info'):
            name = filename[:-len('.egg-info')]
    if name is None:
        raise Exception('Couldn\'t determine the package name for package in %r, is it really a setuptools-enabled package?'%path)
    if os.path.exists(os.path.join(path, '%s.egg-info'%name.replace('-','_'), 'PKG-INFO')):
        pkg_info_path = os.path.join(path, '%s.egg-info'%name.replace('-','_'), 'PKG-INFO')
    elif os.path.exists(os.path.join(path, 'PKG-INFO')):
        pkg_info_path = os.path.join(path, 'PKG-INFO')
    else:
        log.error('No PKG-INFO found for %s in %s', name, path)
        return {}
    fp = open(
        pkg_info_path,
        'rb',
    )
    data = fp.read()
    fp.close()
    pkg_info = {}
    last = None
    for line in data.split('\n'):
        if line.startswith('        '):
            pkg_info[last][-1] += '\n'+line[8:]
        else:
            parts = line.split(': ')
            last = parts[0]
            if not pkg_info.has_key(last):
                pkg_info[last] = []
            value = ': '.join(parts[1:])
            if value.startswith('Development Status :: '):
                pkg_info['Status'] = [value.split('-')[-1].strip()]
            pkg_info[last].append(value)
    return pkg_info

def get_requires(name, path, pip_freeze=False):
    if pip_freeze:
        retval, data = run(
            [
                os.path.join(pyenv, 'bin', 'pip'),
                'freeze',
            ], 
            cwd=os.path.join(pyenv, 'src', name),
        )
    else:
        rp = os.path.join(path, '%s.egg-info'%name, 'requires.txt')
        if not os.path.exists(rp):
            rp = os.path.join(path, '%s.egg-info'%name, 'requires.txt')
        if not os.path.exists(rp):
            log.error('No source code for %r'%name)
            return [] 
        fp = open(rp, 'rb')
        data = fp.read()
        fp.close()
    requires = []
    last = None
    for line in data.split('\n'):
        if line.startswith('['):
            break
        elif not line.strip():
            continue
        else:
            parts = line.split(',')
            first = parts[0]
            for char in ['>','=','<']:
               if char in first:
                   first = first.split(char)[0]
            first = first.strip()
            requires.append(first)
    return requires

def build_html_docs(path, sphinx_build_path=None):
    if sphinx_build_path is not None:
        env=os.environ.copy()
        env['PATH'] = sphinx_build_path+':'+env.get('PATH','')
        return run(
            ['make', 'html'],
            cwd=os.path.join(path, 'doc'),
            env=env,
        )
    else:
        return run(
            ['make', 'html'],
            cwd=os.path.join(path, 'doc')
        )

def copy_html_docs(docs_path, name, path, version):
    dir = os.path.join(docs_path, name.lower())
    if not os.path.exists(dir):
        os.mkdir(dir)
    dst = os.path.join(dir, version)
    if dst == '/':
        raise Exeception('Problem - this would remove your root filesystem')
    if os.path.exists(dst):
        log.debug("REMOVING %s"%dst)
        run(['rm', '-r', dst])
    run(
        [
            'cp',
            '-pr',
            os.path.join(path, 'doc', 'build', 'html'),
            dst,
        ],
    )

def package_index_page(eggs_path, package_docs_path, template_path, pkg_info):
    """\
    docs_path
        the directory containing the docs for all the modules
    dir
        The destination directory for the partcilular package's docs
    pkg_info
        Package Info
    """
    from dreamweavertemplate import DreamweaverTemplateInstance
    name = pkg_info['Name'][0]
    doc_versions = []
    for filename in os.listdir(package_docs_path):
        if os.path.isdir(os.path.join(package_docs_path, filename)):
            doc_versions.append(filename)
    file_versions = {}
    for filename in os.listdir(eggs_path):
        if filename.startswith(name) and filename.endswith('.tar.gz'):
            version = filename[:-len('.tar.gz')].split('-')[1]
            file_versions[version] = (filename, 'tar.gz')
    # Get a template or page
    if os.path.exists(os.path.join(package_docs_path, 'index.html')):
        page = DreamweaverTemplateInstance(
            filename=os.path.join(package_docs_path, 'index.html')
        )
    else:
        page = DreamweaverTemplateInstance(
            filename=template_path,
        )
    # Generate the index page
    page['doctitle'] = '<title>%s</title>'%name
    page['heading'] = name
    summary = pkg_info['Summary'][0]
    if not summary.endswith('.'):
        summary += '.'
    page['content'] = '<p>'+summary+'</p>'
    page['content'] += (
        '<p>Development status :%s, License: %s, Author: %s</p>'
    )%(
        pkg_info['Status'][0],
        pkg_info['License'][0],
        pkg_info['Author'][0]
    )
    page['content'] += '<ul>'
    doc_versions.sort()
    doc_versions.reverse()
    # Add the list of versions for the package
    for i, version in enumerate(doc_versions):
        page['content'] += '<li>'
        if i==0:
            page['content'] += '<b>Latest - '
        else:
            page['content'] += 'Archive - '
        page['content'] += 'Documentation: <a href="%s/index.html">%s</a> '%(
            version, 
            version,
        )
        if file_versions.has_key(version):
            page['content'] += 'Download: '
            filename, type = file_versions[version]
            page['content'] += '<a href="../eggs/%s">%s</a>, '%(
                filename, 
                type
            )
        page['content'] = page['content'][:-2]
        if i==0:
            page['content'] += '</b>'
        page['content'] += '</li>'
    page['content'] += '</ul>'
    # Save the page
    page.save_as_page(
        filename=os.path.join(package_docs_path, 'index.html'),
    )

def egg_index_page(docs_path, template_path, eggs_path, copy_eggs=False, eggs_dir='eggs'):
    from dreamweavertemplate import DreamweaverTemplateInstance
    if not os.path.exists(os.path.join(docs_path, eggs_dir)):
        os.mkdir(os.path.join(docs_path, eggs_dir))
    if copy_eggs:
        filenames = []
        for filename in os.listdir(eggs_path):
            if filename.endswith('.tar.gz') or filename.endswith('.egg'):
                filenames.append(os.path.join(eggs_path, filename))
        copy_files_to(filenames, os.path.join(docs_path, eggs_dir))
    names = []
    for filename in os.listdir(os.path.join(docs_path, eggs_dir)):
        if filename.endswith('.tar.gz'):
            names.append(filename)
    if os.path.exists(os.path.join(docs_path, eggs_dir, 'index.html')):
        page = DreamweaverTemplateInstance(
            filename=os.path.join(docs_path, eggs_dir, 'index.html')
        )
    else:
        page = DreamweaverTemplateInstance(
            filename=template_path
        )
    page['doctitle'] = '<title>%s</title>'%'Eggs'
    page['heading'] = 'Eggs'
    page['content'] = '<ul>'
    names.sort()
    for i, name in enumerate(names):
        page['content'] += '<li>'
        page['content'] +=  '<a href="%s">%s</a>'%(name, name)
    page['content'] += '</ul>'
    page.save_as_page(
        filename=os.path.join(docs_path, eggs_dir, 'index.html')
    )

def main_index_page(docs_path, template_path, exclude=None):
    from dreamweavertemplate import DreamweaverTemplateInstance
    if exclude is None:
        exclude=[]
    # We don't treat the eggs dir as a package
    exclude.append('eggs')
    versions = []
    for filename in os.listdir(docs_path):
        if filename not in exclude and \
           os.path.isdir(os.path.join(docs_path, filename)):
            versions.append(filename)
    if os.path.exists(os.path.join(docs_path, 'index.html')):
        page = DreamweaverTemplateInstance(
            filename=os.path.join(docs_path, 'index.html')
        )
    else:
        page = DreamweaverTemplateInstance(
            filename=template_path
        )
    name = 'Code'
    page['doctitle'] = '<title>%s</title>'%name
    page['heading'] = name
    data = page['content']
    top = data[:data.find('<ul>')]
    last = data[data.find('</ul>')+5:]
    page['content'] = top+'<ul>'
    versions.sort()
    for i, version in enumerate(versions):
        page['content'] += '<li><a href="%s/index.html">%s</a> %s</li>'%(
            version, 
            version, 
            '',
        )
    page['content'] += '</ul>'+last
    page.save_as_page(
        filename=os.path.join(docs_path, 'index.html')
    )

