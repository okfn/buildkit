import base64
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
