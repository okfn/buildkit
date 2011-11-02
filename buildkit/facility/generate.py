"""\
Scan a directory structure to generate a Python filename which when executed will
generate a similar directory structure but with folders and filename contents
renamed according to various options.

Effectively this module helps you quickly write code to generate directory
structures from a template.

See the full documentation in ``../doc/source/manual.rst`` and the example in ``../example``
"""

import os
import base64
from buildkit import facilify

def replace(generate, string, replacements, vars_used):
    used = []
    find_string = string[:]
    string = string.replace('%', '%%').replace('\\','\\\\')
    for k in replacements.keys():
        # Not the best algorithm, but will do for now
        if k in ['--XXXXX--']:
            raise Exception('The key name cannot be %r'%k)
        if k in find_string:
            find_string = find_string.replace(k, '--XXXXX--')
            used.append(k)
            if k not in vars_used:
                vars_used.append(k)
    for k in used:
        string = string.replace(
            k.replace('%', '%%').replace('\\','\\\\'),
            '%('+replacements[k]+')s',
        )
    return string

def exclude(
    generate,
    exclude_paths,
    path
):
    exclude = False
    for exclude_path in exclude_paths:
        if facilify.uniform_path(path) == exclude_path:
            exclude = True
            break
        elif exclude_path.endswith('/') and \
           facilify.uniform_path(path).startswith(exclude_path):
            exclude = True
            break
    return exclude

def prepare(
    generate,
    start_path, 
    replacements=None,
    ignore_extensions=[],
    exclude_paths=[],
    binary_extensions=[],
):
    exclude_paths = [facilify.uniform_path(path) for path in exclude_paths]
    if not os.path.exists(start_path) or not os.path.isdir(start_path):
        raise Exception('No such directory %r'%start_path)
    if replacements is None:
        replacements = {}
    if start_path.endswith(os.sep):
        start_path = start_path[:-1]
    for k, v in replacements.items():
        for other_key, other_value in replacements.items():
            if k != other_key:
                if k in other_key:
                    raise Exception(
                        'The replacement of %r with %r is not guaranteed '
                        'becuase the value is a substring of another value '
                        '%r associated with %r. Please remove one of these '
                        'and correct manually afterwards.' % (
                            v, k, other_key, other_value
                        )
                    )
    vars_used = []
    templates = []
    paths = []
    for dirpath, dirnames, filenames in os.walk(start_path):
        for dirname in dirnames:
            path = os.path.join(dirpath, dirname)
            if generate.exclude(exclude_paths, path):
                continue
            relpath = facilify.relpath(path, start_path)
            if path and not path in paths:
                paths.append(relpath)
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            relpath = facilify.relpath(path, start_path)
            if generate.exclude(exclude_paths, path):
                continue
            ext = filename.split('.')[-1]
            if ext in ignore_extensions:
                continue
            fp = open(path, 'rb')
            content = fp.read()
            fp.close()
            if ext in binary_extensions:
                templates.append(
                    (
                        relpath, 
                        base64.standard_b64encode(content),  
                        True,
                    ) 
                )
            else:
                templates.append(
                    (
                        relpath,
                        generate.replace(content, replacements, vars_used),
                        False,
                    )
                )
    failed_to_use = []
    for item in replacements.keys():
        if item not in vars_used:
            failed_to_use.append(item)
    if failed_to_use:
        raise Exception(
            'Did not use these replacements: %r'%(
                failed_to_use,
            )
        )
    return facilify.obj(
        templates = templates,
        paths = paths,
        vars_used = vars_used,
        replacements = replacements,
    )

def render(
    generate,
    templates, 
    paths,
    vars_used,
    replacements,
):
    output = []
    output.append("import base64")
    output.append("import os")
    output.append("import sys")
    output.append("")
    output.append("templates={")
    for file_path, template, is_binary in templates:
        output.append("    '%s': '''%s''',"%(file_path, template.replace("'", r"\'").replace('"', r'\"')))
    output.append('}')
    output.append("")
    output.append("def render(replacements=None, base_path=None):")
    output.append("    template_vars = {%s}"%(', '.join(["'%s': '%s'"%(replacements[k], k) for k in vars_used])))
    output.append("    if replacements is not None:")
    output.append("        template_vars.update(replacements)")
    output.append("    if base_path is None:")
    output.append("        base_path = os.getcwd()")
    output.append("    elif not os.path.exists(base_path):")
    output.append("        os.mkdir(base_path)")
    for path in paths:
        path_string = generate.replace(path, replacements, vars_used)
        output.append('    if os.path.exists(os.path.join(base_path, "%s"%%dict(template_vars))):'%(path_string,))
        output.append('        raise Exception("Directory already exists: %%s" %% (os.path.join(base_path, "%s"%%dict(template_vars))))'%(
            path_string,
        ))
        output.append('    os.mkdir(os.path.join(base_path, "%s"%%dict(template_vars)))'%(path_string,))
    for file_path, template, is_binary in templates:
        path_string = generate.replace(file_path, replacements, vars_used)
        if is_binary: 
            content = 'base64.standard_b64decode(templates[\'%s\'])'%file_path
        else:
            content = 'templates[\'%s\']%%dict(template_vars)'%file_path
        output.append("""\
    if os.path.exists(os.path.join(base_path, '%s'%%dict(template_vars))):
        raise Exception('File already exists: %%s' %% os.path.join(base_path, '%s'%%dict(template_vars)))
    fp = open(os.path.join(base_path, '%s'%%dict(template_vars)), 'wb')
    fp.write(%s)
    fp.close()"""%(
                path_string,
                path_string,
                path_string,
                content,
            )
        )
    output.append("    return template_vars")
    output.append("")
    output.append('if __name__ == "__main__" and len(sys.argv)>1 and not os.path.exists(sys.argv[1]):')
    output.append('    print "Creating template ..."')
    output.append('    render(base_path=sys.argv[1])')
    output.append('    print "done."')
    final = '\n'.join(output)
    return final

