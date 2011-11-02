from buildkit import facilify
import sys
import os

run_args = facilify.obj(
    summary = 'Perform common tasks relating to generating and building Python packages',
    child_command_specs = facilify.find_commands(
        '%s.command'%__package__, 
        os.path.join(os.path.dirname(__file__), 'command'),
    ),
    facility_specs = [
        {  
            'name': 'dist',
            'spec': 'buildkit.facility.dist',
        },
        {  
            'name': 'repo',
            'spec': 'buildkit.facility.repo',
        },
        {  
            'name': 'generate',
            'spec': 'buildkit.facility.generate',
        },
        {  
            'name': 'scm',
            'spec': 'buildkit.facility.scm',
        },
        {  
            'name': 'start',
            'spec': 'buildkit.facility.start',
        },
    ],
)

if __name__ == '__main__':
    result = facilify.run(**run_args)
    sys.exit(result)



