try:
    import stacks
except:
    import os
    import sys
    localstacks_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), 'localstacks'))
    sys.path.append(localstacks_dir)
    import stacks
