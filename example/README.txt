``build.py``
    Build a set of packages laid out in the directory structure described in
    the manual

``new_package.py``
    Create a new package (you'll need to move all the files within it to a
    ``trunk`` directory for it to be compatible with BuildKit but this is
    handled by ``package_to_repo.py``)

``package_to_repo.py``
    Turn a package created by ``new_package.py`` into a mercurial repository
    capable of being handled by BuildKit and the ``build.py`` script.
