"""\
Recurse through a directory structure to generate template code which
re-generates that structure when run
"""

import os
from buildkit import facilify

arg_specs = [
    dict(
        metavar='DIR',
        help_msg=(
            'The directory containing the source you want to use '
            'as the basis for a template'
        ),
    ),
    dict(
        min=0,
        metavar='REPLACEMENT_PAIRS',
        help_msg = 'Sets of VALUE REPLACEMENT pairs for any strings you wish to treat as variables in the generated template',
    ),
]

opt_specs_by_name = {
    'output': dict(
        flags = ['-o', '--output'],
        help_msg = 'Write the output to FILE',
        metavar = 'FILE',
    ),
    'force': dict(
        flags = ['-f', '--force'],
        help_msg = 'Overwrite OUTPUT_FILE if it already exists',
    ),
    'ignore_extensions': dict(
        flags = ['-i', '--ignore-extensions'],
        help_msg = 'Ignore files with this extension (eg to exclude `file.ignore\', IGNORE should be `ignore\')',
        multiple=True,
        metavar='IGNORE',
    ),
    'exclude_paths': dict(
        flags = ['-x', '--exclude-path'],
        help_msg = 'Exclude a file or directory PATH from the generated template. PATH should be the path relative to the directory the command is run from, not relative to the DIR argument.',
        multiple=True,
        metavar='PATH',
    ),
    'binary_extensions': dict(
        flags = ['-b', '--binary-extensions'],
        help_msg = 'Treat files with this extension as binary (eg to treat `file.png\' as binary, BINARY should be `png\'). Binary files cannot have contents replaced.',
        multiple=True,
        metavar='BINARY',
    ),
}

def run(cmd):
    if len(cmd.args[1:])%2:
        cmd.err("ERROR: Expected an even number of replacement pairs as arguments, not %r", cmd.args[1:])
        return 1
    if not os.path.exists(cmd.args[0]):
        cmd.err("ERROR: No such directory %r", cmd.args[0])
        return 1
    if cmd.opts.output and os.path.exists(cmd.opts.output) and not cmd.opts.force:
        cmd.err("ERROR: File %r already exists, use `-f\' to overwrite", cmd.opts.output)
        return 1
    for ext in cmd.opts.ignore_extensions + cmd.opts.binary_extensions:
        if ext.startswith('.'):
            cmd.err("ERROR: Extension %r is invalid, it shouldn\'t stat with a `.'", ext)
            return 1
    pairs = cmd.args[1:]
    replacements = {}
    while len(pairs):
        if replacements.has_key(pairs[0]):
            cmd.err("ERROR: The replacement key %r has been specified more than once", pairs[0])
            return 1
        replacements[pairs[0]] = pairs[1]
        pairs = pairs[2:]
    result = cmd.generate.prepare(
        cmd.args[0],
        replacements = replacements,
        binary_extensions=cmd.opts.binary_extensions,
        ignore_extensions=cmd.opts.ignore_extensions,
        exclude_paths=cmd.opts.exclude_paths,
    )
    output = cmd.generate.render(**result)
    if cmd.opts.output:
        fp = open(cmd.opts.output, 'w')
        fp.write(output)
        fp.close()
    else:
        cmd.out(output)

