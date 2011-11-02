import os
import shutil

from buildkit import facilify

def run(scm, cmd, path, error_msg):
    res = facilify.process(cmd, cwd=path, merge=True)
    if res.retcode != 0:
        scm.log.error(str(cmd))
        scm.log.error(res.stdout)
        raise Exception(error_msg)
    return res

_IGNORE = '''\
*.DS_Store
.svn
*.svn
.bzr
.coverage
*.swp
*.swo
*.pyc
*.egg-info
*.EGG-INFO
*.db
ez_setup
*~
build/
dist/
data/
doc/build/
'''

_HG_IGNORE = '''\
syntax:glob
.git
''' + _IGNORE

_HG_RC='''\
[web]
allow_push = %(allow_push)s
style = custom
allow_archive = bz2 gz zip
description = %(description)s
'''

def hg(
    scm, 
    path, 
    description, 
    allow_push, 
):
    fp = open(os.path.join(path, '.hgignore'), 'wb')
    fp.write(_HG_IGNORE)
    fp.close()
    scm.run( 
        ['hg', 'init'], 
        path, 
        "Failed to initialise the mercurial repository",
    )
    fp = open(os.path.join(path, '.hg', 'hgrc'), 'wb')
    fp.write(
        _HG_RC%dict(
            allow_push=allow_push,
            description=description,
        )
    )
    fp.close()
    scm.run(
        ['hg', 'add', '.'], 
        path, 
        "Failed to add files to the repository",
    )
    scm.run(
        ['hg', 'add', '.hgignore'],
        path, 
        "Failed to add the .hgignore file",
    )
    scm.run(
        ['hg', 'ci', '-m', 'Initial creation of the repository'], 
        path, 
        "Failed to commit to the repository",
    )

_GIT_IGNORE = """\
.hg
"""+_IGNORE

def git(
    scm, 
    path, 
    description, 
):
    fp = open(os.path.join(path, '.gitignore'), 'wb')
    fp.write(_GIT_IGNORE)
    fp.close()
    scm.run(
        ['git', 'init'], 
        path, 
        "Failed to initialise the git repository"
    )
    scm.run(
        ['git', 'add', '.'], 
        path,
        "Failed to add files to the repository",
    )
    scm.run(
        ['git', 'add', '.gitignore'], 
        path, 
        "Failed to add the .gitignore file",
    )
    scm.run(
        [
            'git', 'commit', 
            '-m', 'Initial creation of the repository', 
        ], 
        path,
        "Failed to commit to the repository",
    )

def git_flow(
    scm, 
    path, 
    description, 
):
    fp = open(os.path.join(path, '.gitignore'), 'wb')
    fp.write(_GIT_IGNORE)
    fp.close()
    #cwd = os.getcwd()
    #os.chdir(path)
    #os.system('git flow init -d')
    scm.run(
        ['git', 'flow', 'init', '-d'],
        path, 
        "Failed to intialise the git-flow repository",
    )
    scm.run(
        ['git', 'add', '.'], 
        path, 
        "Failed to add files to the repository",
    )
    scm.run(
        ['git', 'add', '.gitignore'], 
        path,  
        "Failed to add the .gitignore file",
    )
    scm.run(
        [
            'git', 'commit', 
            '-m', 'Initial creation of the repository', 
        ], 
        path,
        "Failed to commit to the repository",
    )


