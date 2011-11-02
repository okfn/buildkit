import logging
logging.basicConfig(level=logging.ERROR)
import sys; sys.path.insert(0, '../')

if __name__ == "__main__":

    # Normal doctests
    #import doctest
    #doctest.testmod(facilify, optionflags=doctest.ELLIPSIS)
    #doctest.run_docstring_examples(
    #    facilify.parse_argv, facilify.__dict__
    #)

    # Facilify tests
    from buildkit import facilify
    from buildkit.run import run_args
    stack = facilify.SharedStack(
        facility_specs = run_args.facility_specs,
    )
    testLoader = facilify.TestLoader(stack)
    facilify.TestProgram(testLoader, module="command")

