Using BuildKit with BitBucket to create a new repository
++++++++++++++++++++++++++++++++++++++++++++++++++++++++


First get buildkit:

::

    pip install -e BuildKit


On BitBucket, log in and click "+ Create new" on the top of the "Repositories" tab on the top right. Enter your details and click "Create repository".

Clone your repository to your local machine based on the URL bitbucket gives you at the top of your repository.

::

    hg clone https://thejimmyg@bitbucket.org/thejimmyg/jsonpdataproxy

Then in the ``examples`` directory, edit ``new_package.py`` to create the script you want. Make sure the package name and module name are the same as the one Bitbucket created, in this case ``jsonpdataproxy``.

Run this:

::

    python BuildKit/examples/new_package.py

Your empty package will be populated with the new files. Now add them:

::

    cd jsonpdataproxy
    hg add *
    hg ci -m "Initial commit" --user james@feynman
    hg push

You'll need to enter your password. Here's the output:

::

    pushing to https://thejimmyg@bitbucket.org/thejimmyg/jsonpdataproxy
    searching for changes
    http authorization required
    realm: Bitbucket.org HTTP
    user: thejimmyg
    password: 
    adding changesets
    adding manifests
    adding file changes
    added 1 changesets with 17 changes to 17 files



