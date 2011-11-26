from buildkit import stacks
import sys
import os

run_args = stacks.obj(
    summary = 'Perform common tasks relating to generating and building Python packages',
    child_command_specs = stacks.find_commands(
        '%s.command'%__package__, 
        os.path.join(os.path.dirname(__file__), 'command'),
    ),
    facility_specs = stacks.find_facilities(
        '%s.command'%__package__, 
        os.path.join(os.path.dirname(__file__), 'facility'),
    ),
)

if __name__ == '__main__':
    result = stacks.run(**run_args)
    sys.exit(result)

