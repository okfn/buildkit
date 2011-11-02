Manual
++++++

.. contents ::

Differences To Other Software
=============================

BuildKit is really 4 pieces of software in one. It has code for 

* creating a template from a directory structure that can be used to generate similar directory structures
* generating an empty Python package set up for use with ``pip``, ``sphinx`` and ``pypi`` with tests, doctests and packagable as a ``.deb`` file
* setting up packages to use the ``git-flow`` methodology and hosting those projects
* maintaining a website with different versions of different packages' documentation available and links to the downloads
* automatically generating ``.deb`` packages for a Python package and all its dependencies
* running Python tests and generating both Python ``.egg`` and source releases for a package
* setting up and managing a sophisticated test and release infrastructure using Debian packages, Debian apt repositories and KVM virtualisation

Other tools also to some of these things. For example, you may also be interested in:

``python-apt``

    Tools for managing built packages in an ``apt`` environment

``alien``

    Can automatically build a ``.deb`` from a Python package 
    build with ``python setup.py bdist``.

Buildkit Tutorial
=================

BuildKit is installed as a Debian package and only works on Ubuntu LTS. At the
moment it is hosted at apt.okfn.org since it was used for packaging CKAN but
that will change imminently.

You can install it on Ubuntu LTS like this:

::

    sudo -s
    echo 'deb http://apt.okfn.org/ckan-1.4.3.1 lucid universe' > /etc/apt/sources.list.d/okfn.list
    wget -qO-  http://apt.okfn.org/packages.okfn.key | sudo apt-key add -
    apt-get update
    apt-get install buildkit
    
When the email configuration pops up choose "Internet Site" then accept the
hostname suggested (or choose your own).

You'll most likely see this as part of the install:

::

    Creating key in /var/lib/buildkit/key with name BuildKit-Automatic-Packaging, email buildkit@example.com, passphrase buildkit and comment BuildKitkey ...
    Working to create /var/lib/buildkit/key ...
    gpg: directory `/home/james/.gnupg' created
    gpg: new configuration file `/home/james/.gnupg/gpg.conf' created
    gpg: WARNING: options in `/home/james/.gnupg/gpg.conf' are not yet active during this run
    gpg: keyring `/home/james/.gnupg/secring.gpg' created
    gpg: keyring `/home/james/.gnupg/pubring.gpg' created
    gpg: Generating a basic OpenPGP key for buildkit, THIS CAN TAKE A FEW MINUTES if there is not enough entropy ...
    gpg: skipping control `%no-protection' ()
    .+++++++++++++++.++++++++++..++++++++++++++++++++.++++++++++.++++++++++++++++++++++++++++++.++++++++++.++++++++++++++++++++..+++++.++++++++++>.++++++++++.....................................+++++
    
    Not enough random bytes available.  Please do some other work to give
    the OS a chance to collect more entropy!  (Need 280 more bytes)


You just need to do some other work for a minute or two. Perhaps type on the
keyboard or copy a file, check email etc. Eventually gpg will collect enough
entropy and generate you a key which it uses to sign your packages.

QUESTION: Does the buildkit install leave you at a root prompt by mistake?

The default install assumes you will be setting the "buildkit.repo" hostname to
whichever system you will host your repository on and run VMs on. In this case
this will be localhost so edit ``/etc/hosts`` to add the "buildkit.repo" domain
to 127.0.0.1:

    127.0.0.1       localhost buildkit.repo

At this point your repository will be running at http://buildkit.repo and
apt-proxy will be installed and running at http://buildkit.repo:9999/ . The
latter will give you an error about not enough slashes in the URL if you visit
it because it only expects to be visited with a full package path.

If you want git-flow support you'll now need to run:

::

    sudo buildkit-gitflow-installer

Check you have support for KVM:

::

    $ kvm-ok
    INFO: Your CPU supports KVM extensions
    INFO: /dev/kvm exists
    KVM acceleration can be used

You can create a VM without KVM support but you won't be able to run it. Here's
how you create one (the --proxy argument should be the IP address of the system
running apt-proxy, in this case your local machine):

::

    sudo buildkit vm create --proxy 192.168.0.6 -o /var/lib/buildkit/vm/ 10

You can check that apt-proxy has been used like this:

::

    sudo ls /var/cache/apt-proxy/ubuntu/pool/main/

If the directory exists and is populated, the files from here will be used next
time you create a VM. The creation takes nearly as long though because files
are still pulled in over HTTP, just served from apt-proxy rather than direclty.
It does save bandwidth though.

In reality it is usually easier to just copy the ``.qcow2`` VM disk file to create
a new VM. Let's keep this one as a base VM:

::

    export IMAGE=`sudo ls /var/lib/buildkit/vm/buildkit10/ | awk '{print $0}' | grep -v "run.sh"`
    sudo cp -p /var/lib/buildkit/vm/buildkit10/${IMAGE} /var/lib/buildkit/vm/base.qcow2

Whenever you want a new VM you can then just run:

::

    qemu-img convert -f qcow2 -O raw /var/lib/buildkit/vm/base.qcow2 /var/lib/buildkit/vm/new/disk.raw
    
This converts from the small .qcow2 file to a fresh ``disk.raw`` image.

Now let's start it (change eth1 for your network interface):

::

    sudo buildkit-vm-start eth1 qtap0 512M 1 /var/lib/buildkit/vm/buildkit10/disk.raw

Now you can connect from the host to the guest over SSH:

::

    ssh ubuntu@192.168.100.10

The  username and password for the VM are both ``ubuntu``. You can also use
``sudo -s`` with the password  ``ubuntu`` to get root access. You may want to
change the password with ``passwd``.

Possible future BuildKit enhancements
=====================================

* Make the buildkit-vm-create command part of the buildkit command
* Swap apt-proxy for something that also caches downoads from virutal machines
  (it currently gives bad header lines which seems to be a known, yet
  unresolved issue)

More help
=========

More documentation to come, at the moment you can work out most of what you
need by browsing the online help starting at:

::

    buildkit --help

