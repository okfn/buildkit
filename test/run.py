import logging
logging.basicConfig(level=logging.ERROR)
import sys; sys.path.insert(0, '../')

if __name__ == "__main__":

    # Normal doctests
    #import doctest
    #doctest.testmod(stacks, optionflags=doctest.ELLIPSIS)
    #doctest.run_docstring_examples(
    #    stacks.parse_argv, stacks.__dict__
    #)

    # Facilify tests
    from buildkit import stacks
    from buildkit.run import run_args
    stack = stacks.SharedStack(
        facility_specs = run_args.facility_specs,
    )
    testLoader = stacks.TestLoader(stack)
    stacks.TestProgram(testLoader, module="command")

