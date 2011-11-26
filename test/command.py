import difflib
import shutil
import os
import sys

from buildkit import stacks
from buildkit.run import run_args

class TestGenerate(stacks.TestCase):

    def test_01_generate(self):
        expected = r"""import base64
import os
import sys

templates={
    'run.py': '''from b import message

print \"%(LOG_LEVEL)s: %%s\" %% message
''',
    'a1.png': '''iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAAXNSR0IArs4c6QAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9sEGAkQLzrCi3sAAAAZdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAADgElEQVR42u2Zv0vrUBTHv3lRqwi1mKIUBQUdFKlFEQc76OyQQbHgooI4dlAQnPwLXJwFuzkIgqGLIFYQrINVCIilIlbBUsWfUDQSbc6bLC/Key/pD17yeg/c4YTcnHs/N+eec8/liIhQxvIDZS4MAAPAADAADAADwAAwAAwAA8AAMAAMAAPAAFhbTk5OsLy8DFEUUVdXB47jdC0fqbDyhJPJJCKRCHZ2dhCJRHB7e1t0G5yVS2JmVzWfqdjKBVpaWjA5OYlQKIRkMlmUb1ZYfcJDQ0O51traWl4uYNZF/nsXKIWYcoF0Oo2joyPIsoyzszNcXFzg5uYG9/f3eH19haZpcLlcEAQB3d3dGBwcxMjICDwej3UJkAkBYLpVV1dTMBikTCZDxZavtvL6RqkBfDav10tXV1eWA2BqE/zcdNxuN0RRhN/vh8/nQ3NzM1wuF7LZLO7u7hCLxbC2tobNzU1ompbr39vbi4ODA1RVVVlmEzSFbWBggCRJoo+PD0Pv7+3tUWNjo26VFhcX7esC+cjh4SFVVlbmBikIAimKYhkAJQ+DfX19mJqayukPDw+QJKm8ToOBQECn7+/vlxcAn8+n02OxWHkBEARBp6dSKXtmgr/K8fExwuEwZFlGPB7H4+MjMpkMFEX5a9/n52d7ZoJERJIkUWdnZ0FJEcdx9guD2WyWZmZmCpp4oYMtBQDDLjA/P4+VlRXdM4/Hg7GxMfj9frS3t6OpqQm1tbWoqakBz/MFVXcs5QKyLBPP8zraCwsLpKqqIcovLy+W/QMM9ZqdndUZCgQCpoxcX19bFoChMLi9va3Tg8Ggqb/s9PTU3vcCX+O21+s1ZcRKmV9eNUGHwwFVVXP629sbHA6HIQOapqGtrQ2Xl5eFH13/VU3Q7Xbr9EQiYdhAKBT6NnnbuUBPT8+3SRmRRCKBubk5a1dFjeyUq6urut2W53na2Nj4Y59oNPqtGGLbMPj+/k4dHR3f0tmJiQna3d2lp6cnUlWVUqkUhcNhGh8fJ47jcu9OT0/bGwARUTwep/r6etMp7+joKKmqmvdgS516m8J2fn5O/f39hgw6nU5aWloiTdMKWq1SA8jramxrawvr6+uIRqNIp9NQFAWCIKChoQFdXV0QRRHDw8NwOp0Fh6xinSF+Z8/Wd4O2qQgxAAwAA8AAMAAMAAPAADAADAADwABYTX4C3JAjt3gTqkQAAAAASUVORK5CYII=''',
    'B/__init__.py': '''from .b import message
''',
    'B/b.py': '''from .%(C)s import message
''',
    'B/B.py': '''message = \'\'\'\'hello, world! * & %% \"\"\" \" \'\'\'\'
''',
}

def render(replacements=None, base_path=None):
    template_vars = {'LOG_LEVEL': 'OUTPUT', 'C': 'B'}
    if replacements is not None:
        template_vars.update(replacements)
    if base_path is None:
        base_path = os.getcwd()
    elif not os.path.exists(base_path):
        os.mkdir(base_path)
    if os.path.exists(os.path.join(base_path, "%(C)s"%dict(template_vars))):
        raise Exception("Directory already exists: %s" % (os.path.join(base_path, "%(C)s"%dict(template_vars))))
    os.mkdir(os.path.join(base_path, "%(C)s"%dict(template_vars)))
    if os.path.exists(os.path.join(base_path, 'run.py'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'run.py'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'run.py'%dict(template_vars)), 'wb')
    fp.write(templates['run.py']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'a1.png'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'a1.png'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'a1.png'%dict(template_vars)), 'wb')
    fp.write(base64.standard_b64decode(templates['a1.png']))
    fp.close()
    if os.path.exists(os.path.join(base_path, '%(C)s/__init__.py'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, '%(C)s/__init__.py'%dict(template_vars)))
    fp = open(os.path.join(base_path, '%(C)s/__init__.py'%dict(template_vars)), 'wb')
    fp.write(templates['B/__init__.py']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, '%(C)s/b.py'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, '%(C)s/b.py'%dict(template_vars)))
    fp = open(os.path.join(base_path, '%(C)s/b.py'%dict(template_vars)), 'wb')
    fp.write(templates['B/b.py']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, '%(C)s/%(C)s.py'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, '%(C)s/%(C)s.py'%dict(template_vars)))
    fp = open(os.path.join(base_path, '%(C)s/%(C)s.py'%dict(template_vars)), 'wb')
    fp.write(templates['B/B.py']%dict(template_vars))
    fp.close()
    return template_vars

if __name__ == "__main__" and len(sys.argv)>1 and not os.path.exists(sys.argv[1]):
    print "Creating template ..."
    render(base_path=sys.argv[1])
    print "done."
"""
        here = stacks.uniform_path(os.path.dirname(__file__))
        output = []
        def out(*k, **p):
            output.append(stacks.format_string(*k, **p))
        result = stacks.run(
            argv=['generate', '--binary', 'png', '--ignore', 'ignore', 'generate_src', 'OUTPUT', 'LOG_LEVEL', 'B', 'C'],
            out=out,
            err=out,
            **run_args
        )
        self.assertEqual(result, 0)
        self.assertEqual(len(output), 1)
        for line in difflib.unified_diff(
            expected.split('\n'), 
            output[0].split('\n'),
        ):
            print line
        self.assertEqual(''.join(output), expected)
        # Now test that when we execute the file it generates the correct directory structure
        if os.path.exists(os.path.join(here, 'generate.py')):
            os.remove(os.path.join(here, 'generate.py'))
        if os.path.exists(os.path.join(here, 'generate_dst')):
            shutil.rmtree(os.path.join(here, 'generate_dst'))
        fp = open(os.path.join(here, 'generate.py'), 'wb')
        fp.write(''.join(output))
        fp.close()
        cmd = [
            sys.executable, 
            os.path.join(here, 'generate.py'),
            'generate_dst',
        ]
        stacks.process(cmd)
        # Now check that the directory structure is identical apart from the ignored file
        cmd = "diff -ru generate_src/ generate_dst/"
        result = stacks.process(cmd.split(' '))
        self.assertEqual(result.stdout, "Only in generate_src/: a1.ignore\n")

    def test_02_start(self):
        expected = """\
running bdist_egg
running egg_info
creating generated_package.egg-info
writing generated_package.egg-info/PKG-INFO
writing top-level names to generated_package.egg-info/top_level.txt
writing dependency_links to generated_package.egg-info/dependency_links.txt
writing entry points to generated_package.egg-info/entry_points.txt
writing manifest file 'generated_package.egg-info/SOURCES.txt'
reading manifest file 'generated_package.egg-info/SOURCES.txt'
reading manifest template 'MANIFEST.in'
warning: no files found matching 'example/*.py'
warning: no files found matching 'ez_setup.py'
writing manifest file 'generated_package.egg-info/SOURCES.txt'
installing library code to build/bdist.linux-x86_64/egg
running install_lib
running build_py
creating build
creating build/lib.linux-x86_64-2.6
creating build/lib.linux-x86_64-2.6/generated_package
copying generated_package/__init__.py -> build/lib.linux-x86_64-2.6/generated_package
creating build/bdist.linux-x86_64
creating build/bdist.linux-x86_64/egg
creating build/bdist.linux-x86_64/egg/generated_package
copying build/lib.linux-x86_64-2.6/generated_package/__init__.py -> build/bdist.linux-x86_64/egg/generated_package
byte-compiling build/bdist.linux-x86_64/egg/generated_package/__init__.py to __init__.pyc
creating build/bdist.linux-x86_64/egg/EGG-INFO
copying generated_package.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
copying generated_package.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying generated_package.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying generated_package.egg-info/entry_points.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
copying generated_package.egg-info/not-zip-safe -> build/bdist.linux-x86_64/egg/EGG-INFO
copying generated_package.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
creating dist
creating 'dist/generated_package-0.1.2-py2.6.egg' and adding 'build/bdist.linux-x86_64/egg' to it
removing 'build/bdist.linux-x86_64/egg' (and everything under it)
"""
        here = stacks.uniform_path(os.path.dirname(__file__))
        if os.path.exists(os.path.join(here, 'generate_package')):
            shutil.rmtree(os.path.join(here, 'generate_package'))
        output = []
        def out(*k, **p):
            output.append(stacks.format_string(*k, **p))
        result = stacks.run(
            argv=[
                'start', 
                '--git',
                '--author-name', 'James Gardner',
                '--author-email', 'james@jimmyg.org',
                '--version', '0.1.2', 
                'generated_package',
                'James\'s test package',
                os.path.join(here, 'generate_package'),
            ],
            out=out,
            err=out,
            **run_args
        )
        self.assertEqual(result, 0)
        self.assertEqual(len(output), 0)
        # Now check that the directory structure is identical apart from the ignored file
        cmd = "python setup.py bdist_egg"
        result = stacks.process(
            cmd.split(' '), 
            cwd=os.path.join(here, 'generate_package')
        )
        for line in difflib.unified_diff(
            expected.split('\n'), 
            result.stdout.split('\n'),
        ):
            print line
        self.assertEqual(result.stdout, expected)

    def test_03_non_python_package(self):
        dirname = 'non_python_package'
        here = stacks.uniform_path(os.path.dirname(__file__))
        if os.path.exists(os.path.join(here, dirname)):
            shutil.rmtree(os.path.join(here, dirname))
        output = []
        def out(*k, **p):
            output.append(stacks.format_string(*k, **p))
        result = stacks.run(
            argv=[
                'pkg', 
                'nonpython', 
                '--deb',
                '--rpm',
                '--output-dir', os.path.join(here, dirname),
                 os.path.join(here, 'non_python_package_src'), 
            ],
            out=out,
            err=out,
            **run_args
        )
        if len(output):
            print output
        self.assertEqual(result, 0)
        self.assertEqual(len(output), 0)
        # Note that the version is hardwired to 0.1.0 in this case in the test control file
        self.assertEqual(os.path.exists(os.path.join(dirname, 'buildkit_0.1.0+01+lucid_all.deb')), True)
        self.assertEqual(os.path.exists(os.path.join(dirname, 'buildkit-0.1.0+01+lucid-2.noarch.rpm')), True)

    def test_04_python_package(self):
        dirname = 'python_package'
        here = stacks.uniform_path(os.path.dirname(__file__))
        if os.path.exists(os.path.join(here, dirname)):
            shutil.rmtree(os.path.join(here, dirname))
        output = []
        def out(*k, **p):
            output.append(stacks.format_string(*k, **p))
        result = stacks.run(
            argv=[
                'pkg', 
                'python', 
                '--rpm',
                '--author-email', 'author@example.com',
                '--packager-email', 'packager@example.com',
                '--author-name', 'James Author',
                '--packager-name', 'James Packager',
                '--deps',
                '--exclude=test/generate_package',
                '--exclude=test.old',
                '--debian-dir',
                '--output-dir', os.path.join(here, dirname),
                '--url', 'http://jimmyg.org/james',
                '-d', 'rsync',
                '-d', 'apache2',
                #'--skip-remove-tmp-dir',
                '../../buildkit', 
            ],
            out=out,
            err=out,
            **run_args
        )
        if len(output):
            print output
        self.assertEqual(result, 0)
        self.assertEqual(len(output), 2)
        print ''.join(output)
        self.assertEqual(os.path.exists(os.path.join(dirname, 'python-buildkit_0.1.2+01+lucid-1_all.deb')), True)
        self.assertEqual(
            os.path.exists(os.path.join(dirname, 'buildkit_0.1.2+01+lucid_debian')),
            True,
        )
        self.assertEqual(
            os.path.isdir(os.path.join(dirname, 'buildkit_0.1.2+01+lucid_debian')),
            True,
        )
        for filename in ['changelog', 'compat', 'control', 'copyright', 'docs', 'rules']:
            path = os.path.join(dirname, 'buildkit_0.1.2+01+lucid_debian', filename)
            self.assertEqual(
                os.path.exists(path),
                True,
            )
            self.assertEqual(
                os.stat(path).st_size>0,
                True,
            )

