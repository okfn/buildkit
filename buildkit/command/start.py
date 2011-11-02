"""\
Generate an empty project template already set up to use BuildKit

You can install ``git-flow`` like this:

::

    wget --no-check-certificate -q -O - https://github.com/nvie/gitflow/raw/develop/contrib/gitflow-installer.sh | sudo sh
    
You'll see output like this:

::

    ### gitflow no-make installer ###
    Installing git-flow to /usr/local/bin
    Cloning repo from GitHub to gitflow
    Initialized empty Git repository in /home/james/Documents/Packages/git/buildkit/test/gitflow/.git/
    remote: Counting objects: 2199, done.
    remote: Compressing objects: 100% (890/890), done.
    remote: Total 2199 (delta 1302), reused 2107 (delta 1220)
    Receiving objects: 100% (2199/2199), 456.51 KiB | 518 KiB/s, done.
    Resolving deltas: 100% (1302/1302), done.
    Updating submodules
    Submodule 'shFlags' (git://github.com/nvie/shFlags.git) registered for path 'shFlags'
    Initialized empty Git repository in /home/james/Documents/Packages/git/buildkit/test/gitflow/shFlags/.git/
    remote: Counting objects: 454, done.
    remote: Compressing objects: 100% (55/55), done.
    remote: Total 454 (delta 389), reused 454 (delta 389)
    Receiving objects: 100% (454/454), 101.30 KiB, done.
    Resolving deltas: 100% (389/389), done.
    Submodule path 'shFlags': checked out '2fb06af13de884e9680f14a00c82e52a67c867f1'
    `gitflow/git-flow' -> `/usr/local/bin/git-flow'
    `gitflow/git-flow-init' -> `/usr/local/bin/git-flow-init'
    `gitflow/git-flow-feature' -> `/usr/local/bin/git-flow-feature'
    `gitflow/git-flow-hotfix' -> `/usr/local/bin/git-flow-hotfix'
    `gitflow/git-flow-release' -> `/usr/local/bin/git-flow-release'
    `gitflow/git-flow-support' -> `/usr/local/bin/git-flow-support'
    `gitflow/git-flow-version' -> `/usr/local/bin/git-flow-version'
    `gitflow/gitflow-common' -> `/usr/local/bin/gitflow-common'
    `gitflow/gitflow-shFlags' -> `/usr/local/bin/gitflow-shFlags'

Then you'll be able to run commands like these:

::

    $ git flow
    usage: git flow <subcommand>
    
    Available subcommands are:
       init      Initialize a new git repo with support for the branching model.
       feature   Manage your feature branches.
       release   Manage your release branches.
       hotfix    Manage your hotfix branches.
       support   Manage your support branches.
       version   Shows version information.
    
    Try 'git flow <subcommand> help' for details.

"""

import datetime
import os
from buildkit import facilify

arg_specs = [
    dict(
        metavar='MODULE_NAME',
        help_msg=(
            'They Python name of the module once it is imported (you can set the PyPi package name separately with the `-p\' option)'
        ),
    ),
    dict(
        metavar='DESCRIPTION',
        help_msg = 'A short, one line description of the package',
    ),
    dict(
        metavar='DIR',
        help_msg=(
            'The directory to generate the new package in'
        ),
    ),
]

opt_specs_by_name = facilify.OrderedDict(
    package = dict(
        flags = ['-p', '--package'],
        help_msg = 'Name of the new package',
        metavar='PACKAGE',
    ),
    version = dict(
        flags = ['-r', '--version'],
        help_msg = 'Package version, defaults to 0.1.0',
        metavar='VERSION',
        default = '0.1.0',
    ),
    url = dict(
        flags = ['-u', '--url'],
        help_msg = 'URL of the project homepage',
        metavar='URL',
    ),
    git = dict(
        flags = ['--git'],
        help_msg = 'Set up the new package as a git repository',
    ),
    git_flow = dict(
        flags = ['--git-flow'],
        help_msg = 'Set up the new package as a git repository following the git-flow methodology',
    ),
    hg = dict(
        flags = ['--hg'],
        help_msg = 'Set up the new package as a mercurial repository',
    ),
    license_name = dict(
        flags = ['-l', '--license-name'],
        help_msg = 'The name of the license. Defaults to "GNU AGPLv3"',
        metavar='LICENSE_NAME',
        default='GNU AGPLv3',
    ),
    author_name = dict(
        flags = ['-a', '--author-name'],
        help_msg = 'Name of the primary author using simple characters (a-z, A-Z, 0-9, hyphen and space)',
        metavar='AUTHOR_NAME',
    ),
    author_email = dict(
        flags = ['-e', '--author-email'],
        help_msg = 'Contact email of the person given in `--author-name\'',
        metavar='AUTHOR_EMAIL',
    ),
    author_url = dict(
        flags = ['--author-url'],
        help_msg = 'Optional homepage of the person given in `--author-name\'',
        metavar='AUTHOR_URL',
    ),
    copyright_year = dict(
        flags = ['-y', '--copyright-year'],
        help_msg = 'The year, or years this work was copyrighted, defaults to the current year',
        metavar='COPYRIGHT_YEAR',
        default=str(datetime.datetime.now().year),
    ),
    changelog_date = dict(
        flags = ['-c', '--changelog-date'],
        help_msg = 'The date of the first changelog entry in the format yyy-mm-dd, defaults to today',
        metavar='CHANGELOG_DATE',
        default=datetime.datetime.now().strftime('YYYY-mm-dd'),
    ),
    distro_depends = dict(
        flags = ['-d', '--distro-dep'],
        help_msg = 'A list of dependencies in the format expected by the distribution, eg for Ubuntu lucid: "apache2, libapache2-mod-wsgi, postgresql-8.4-postgis"',
        multiple=True,
        metavar='DEPENDS',
    ),
    distro_pre_depends = dict(
        flags = ['--distro-pre-dep'],
        help_msg = 'A list of dependencies which must be installed before the dependencies in the formmat expected by the distribution',
        metavar='DISTRO_PRE_DEPENDS',
        multiple=True,
    ),
    distro_section = dict(
        flags = ['--distro-section'],
        help_msg = 'The section this package should appear in within the distribution repository, eg "main/web"',
        metavar='DISTRO_SECTION',
    ),
    distro_package = dict(
        flags = ['--distro-package'],
        help_msg = 'The name the distribution will use for this package, defaults to the module name',
        metavar='DISTRO_PACKAGE',
    ),
    allow_push = dict(
        flags = ['--allow-push'],
        help_msg = 'A comma separated list of usernames who are allowed to push to the repository. Only works when you also specify one of `--hg\', `--git\' or `--git-flow\'',
        metavar='USERNAME_LIST',
    ),
)

def run(cmd):
    scm_no = int(cmd.opts.git) + int(cmd.opts.git_flow) + int(cmd.opts.hg)
    if scm_no > 1:
        cmd.err('ERROR: You can only specify one of `--hg\', `--git\' or `--git-flow\'')
        return 1
    elif not scm_no and cmd.opts.has_key('allow_push'):
        cmd.err('ERROR: The `--allow-push\' option only works when you also specify one of `--hg\', `--git\' or `--git-flow\'')
        return 1
    #elif not cmd.opts.author_name or not cmd.opts.author_email:
    #    cmd.err('ERROR: You must specify `--author-name\' and `--author-email\' when using `--hg\', `--git\' or `--git-flow\'')
    #    return 1
    opts = facilify.strip_none(cmd.opts)
    opts['module'] = cmd.args[0]
    opts['description'] = cmd.args[1]
    opts['distro_depends'] = ", ".join(cmd.opts.distro_depends)
    opts['distro_pre_depends'] = ", ".join(cmd.opts.distro_pre_depends)
    template_vars = cmd.start.generate(opts, cmd.args[2])
    if cmd.opts.hg:
        cmd.scm.hg(
            cmd.args[2], 
            description = template_vars['description'],
            allow_push = template_vars['allow_push'],
       )
    elif cmd.opts.git:
        cmd.scm.git(
            cmd.args[2],
            description = template_vars['description'],
        )
    elif cmd.opts.git_flow:
        cmd.scm.git_flow(
            cmd.args[2],
            description = template_vars['description'],
        )

