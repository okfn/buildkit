"""\
Change the package version numbers in a Python source tree
"""

import datetime
import os
from buildkit import facilify

arg_specs = [
    dict(
        metavar='DIR',
        help_msg=(
            'Directory containing the package setup.py file'
        ),
    ),
    dict(
        metavar='OLD_VERSION',
        help_msg=(
            'Old version number'
        ),
    ),
    dict(
        metavar='NEW_VERSION',
        help_msg=(
            'New version number'
        ),
    ),
]

opt_specs_by_name = {
    'changelog': dict(
        flags = ['-l', '--changelog'],
        help_msg = 'A rst bulleted list of change items eg \'* Updated the release functionality\'',
        metavar = 'CHANGELOG',
        default = '* To add',
    ),
}

def replace(filename, old, new, variable='version'):
    if variable is None:
        regex = "s/%s/%s/"%(old, new)
    else:
        regex = "s,%s[ =].*['\"]%s['\"],%s = '%s',"%(variable, old, variable, new)
    command = [
        'sed',
        '-e',
        regex,
        '-i',
        filename,
    ]
    facilify.process(command)

def run(cmd):
    base_dir = facilify.uniform_path(cmd.args[0])

    if not os.path.exists(base_dir):
        cmd.err("ERROR: No such directory %r", base_dir)
        return 1
    if cmd.args[1] == cmd.args[2]:
        cmd.err('The version numbers must be different')
        return 1
    # The three files that need updating are:
    # setup.py
    setup = os.path.join(base_dir, 'setup.py')
    if not os.path.exists(setup):
        cmd.err("ERROR: Could not find the 'setup.py' file, did you specify the correct directory?")
        return 1
    replace(setup, cmd.args[1], cmd.args[2])
    # doc/source/index.rst
    doc_index = os.path.join(base_dir, 'doc', 'source', 'index.rst')
    if not os.path.exists(doc_index):
        cmd.err('Skipping %r, file not found', doc_index)
    else:
        replace(doc_index, cmd.args[1], cmd.args[2], None)
    # doc/source/conf.py
    conf_py = os.path.join(base_dir, 'doc', 'source', 'conf.py')
    if not os.path.exists(conf_py):
        cmd.err('Skipping %r, file not found', conf_py)
    else:
        replace(conf_py, cmd.args[1], cmd.args[2])
        replace(conf_py, cmd.args[1], cmd.args[2], 'release')
    # Changelog
    changelog = os.path.join(base_dir, 'CHANGELOG.txt')
    if not os.path.exists(changelog):
        cmd.err('Skipping %r, file not found', changelog)
    else:
        data = facilify.file_contents(changelog)
        if '%s\n%s'%(cmd.args[2], '-'*len(cmd.args[2])) in data:
            cmd.err('Skipping %r, aready has a %s section', changelog, cmd.args[2])
        else:
            contents = data.split('\n')
            contents = contents[:2] + [
                '',
                cmd.args[2], 
                len(cmd.args[2])*'-', 
                '', 
                datetime.datetime.now().strftime('%Y-%m-%d'), 
                '~~~~~~~~~~',
                '',
            ] + cmd.opts.changelog.split('\\n') + [''] + contents[2:]
            fp = open(changelog, 'w')
            try:
                fp.write('\n'.join(contents))
                fp.close()
            except:
                fp.write(data)
                fp.close()
                raise
    cmd.out('done.')

