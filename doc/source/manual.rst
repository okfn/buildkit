Manual
++++++

.. contents ::

Differences To Other Software
=============================

BuildKit is really 4 pieces of software in one. It has code for

* creating a template from a directory structure that can be used to generate similar directory structures
* generating an empty Python package set up for use with ``pip``, ``sphinx`` and ``pypi`` with tests, doctests and packagable as a ``.deb`` file
* setting up packages to use the ``git-flow`` methodology and hosting those projects
* automatically generating ``.deb`` packages for a Python package and all its dependencies
* running Python tests and generating both Python ``.egg`` and source releases for a package
* setting up and managing a sophisticated test and release infrastructure using Debian packages, Debian apt repositories and KVM virtualisation

Other tools also do some of these things. For example, you may also be interested in:

``python-apt``

    Tools for managing built packages in an ``apt`` environment

``alien``

    Can automatically build a ``.deb`` from a Python package
    build with ``python setup.py bdist``.

Buildkit also used to do:

* building a sdist release, installing into a clean virtualenv and running tests in isolation
* maintaining a website with different versions of different packages' documentation available and links to the downloads

These features will be added back in a future release.

Buildkit Tutorial
=================

.. caution ::

   Buildkit only works on Ubuntu 10.04 LTS. Any other platform is untested and vitually guaranteed to break. Only use on Ubuntu 10.04.

   Also note that for the VM funtionality to work, you will need virtualisation CPU extensions. You can check you have the necessary support like this:

   ::
       $ sudo apt-get install kvm
       $ kvm-ok
       INFO: Your CPU supports KVM extensions
       INFO: /dev/kvm exists
       KVM acceleration can be used

    You can create a VM without KVM support but you won't be able to run it.

BuildKit is installed as a Debian package so the first thing you need to do is
to use it to create a debian package from the source.

Unzip the source distribution and change to the same directory as ``setup.py``.

Now install all the dependencies listed in
``buildkit_deb/DEBIAN/control.template``. At the time of writing you can do so
like this:

::

    sudo apt-get install ubuntu-vm-builder python-vm-builder gawk kvm sed findutils rsync apache2 reprepro gnupg wget dh-make devscripts build-essential fakeroot alien cdbs python-pip python-virtualenv subversion mercurial git-core apt-proxy kvm-pxe uml-utilities

When the email configuration pops up choose "Internet Site" then accept the
hostname suggested (or choose your own).

Then build the buildkit ``.deb`` files like this:

::

    PACKAGEVERSION=01
    mkdir -p dist/buildkit
    python -m buildkit.run pkg nonpython -p "$PACKAGEVERSION" -o dist/buildkit --deb buildkit_deb
    python -m buildkit.run pkg python -p "$PACKAGEVERSION" -o dist/buildkit --author-email james@pythonweb.org --deb .

You'll then get two ``.deb`` files in ``dist/buildkit`` which you can install:

::

    sudo dpkg -i dist/buildkit/*.deb

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

The default install assumes you will be setting the "host.buildkit" hostname to
whichever system you will host your repository on and run VMs on. In this case
this will be localhost so edit ``/etc/hosts`` to add the "host.buildkit" hostname
to 127.0.0.1:

::

    127.0.0.1       localhost host.buildkit

At this point your repository will be running at http://host.buildkit and
apt-proxy will be installed and running at http://host.buildkit:9999/ . The
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

    IP=`/sbin/ifconfig $NETWORK_DEVICE | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}' | grep -v "127.0.0.1" | grep -v "192.168.100."`
    sudo buildkit vm create --proxy $IP -o /var/lib/buildkit/vm/ 10

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

    export IMAGE=`sudo ls /var/lib/buildkit/vm/buildkit10/ | awk '{print $0}' | grep -v "run.sh" | grep -v "disk.raw"`
    sudo cp -p /var/lib/buildkit/vm/buildkit10/${IMAGE} /var/lib/buildkit/vm/base.qcow2

You can always just copy the VM manually too, you just have to find out what
the image name is in the ``buildkit10`` directory.

Whenever you want a new VM you can then just run:

::

    sudo -u buildkit qemu-img convert -f qcow2 -O raw /var/lib/buildkit/vm/base.qcow2 /var/lib/buildkit/vm/new/disk.raw

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


Example: Building and Testing the CKAN Package Install
======================================================

CKAN is an open source metadata catalogue that powers sites like data.gov.uk
and which uses buildkit for its package install. In this section we'll walk
through how to use buildkit to package it.

Setting up
----------

First you need to get the source code for the version you want to package:

::

    hg clone -r release-v1.5 https://bitbucket.org/okfn/ckan/

Next you need to install buildkit, either from source (as described above) or
from an apt-repository where it is hosted. Once it is installed you'll have an
apt repository running on your local machine as well as the ``buildkit``
command and the ability to boot virtual machines for testing. (You'll need to
build a base VM using the ``buildkit vm create`` command as described above).

The individual buildkit commands that are needed to build CKAN are specified in
the ``build.sh`` script so you should take a look at that.

Creating an apt repository
--------------------------

The ``build.sh`` script exports all the ``.deb`` files that are created to an
apt repository on your local machine that is hosted by Apache and set up as
part of the buildkit install. Before you can run the script you need to create
the repository that will be used:

::

    sudo -u buildkit buildkit repo clone /var/lib/buildkit/repo/base_lucid ckan-1.5

Check that there are no packages in the repository yet:

::

    sudo -u buildkit buildkit repo list /var/lib/buildkit/repo/ckan-1.5

There shouldn't be any output.

Now on to the packaging itself.

Packaging
---------

First edit ``build.sh`` to set the environment variables relevant to you.

Run the build (not as root) like this:

::

    ./build.sh

At the end of the build you'll be prompted for your password so that ``sudo``
can import the packages into the buildkit repository on your local machine to
serve.

You should end up with a set of packages the buildkit repository accessible
from your apt repository as well as a set in ``ckan/dist/buildkit``.

You can now test the build.

Testing
-------

If you've followed the buildkit tutorial and created a base VM, you can now
create a new virtual machine like so:

::

    sudo -u buildkit mkdir /var/lib/buildkit/vm/ckan
    sudo -u buildkit qemu-img convert -f qcow2 -O raw /var/lib/buildkit/vm/base.qcow2 /var/lib/buildkit/vm/ckan/disk.raw

After a few moments you can start your VM (tip: be sure to specify the correct network interface that the VM should use to access the internet, in this case I've used ``eth1``, yours might be ``eth0``).

::

    sudo buildkit-vm-start eth1 qtap0 1024M 4 /var/lib/buildkit/vm/ckan/disk.raw

Here I'm giving the VM 1024M and letting it use 4 CPUs. For a production CKAN
you should have at least 1.5Gb of RAM.

.. tip ::

    If a QEMU window appears but nothing happens after a few seconds it is
    likely your CPU doesn't support virtualisation extensions needed by KVM. Run
    the ``kvm-ok`` command mentioned earlier to check.

    If KVM isn't supported you could try using virtualbox instead. Start by
    installing VirtualBox:

    ::

        sudo apt-get install virtualbox-ose
        sudo rmmod kvm-intel
        # Or if you have an AMD machine:
        # sudo rmmod kvm-amd

    Then convert the disk image to a ``.vdi`` file:

    ::

        sudo -u buildkit qemu-img convert -f qcow2 -O vdi /var/lib/buildkit/vm/base.qcow2 /var/lib/buildkit/vm/ckan/disk.vdi

    Then use the interface to create a new Ubuntu 10.04 machine with this disk
    image as its base. The networking setup will be different if you use virtualbox
    and you'll need to edit the various ``/etc/hosts`` files yourself to be able to
    test your CKAN install, but if you are a virtualbox expert, it should be
    possible.

    See here for a port forwarding approach that is useful: http://jimmyg.org/blog/2008/ssh-to-a-debian-etch-virtual-machine-in-virtualbox.html

    The alternative is just to install CKAN onto your host machine for testing
    and not worry about VMs at all.

Assuming the ``buildkit-vm-start`` command worked you can now connect from the
host to the guest over SSH:

::

    ssh ubuntu@192.168.100.10

Or if you have installed buildkit as standard and not changed any network
settings you can use the ``default.vm.buildkit`` hostname that buildkit set up
for you when it was installed:

::

    ssh ubuntu@default.vm.buildkit

The  username and password for the VM are both ``ubuntu``. You can also use
``sudo -s`` with the password  ``ubuntu`` to get root access. You may want to
change the password with ``passwd``.

Optionally, you might want to install some common software at this point such
as vim, screen, elinks or any other software you commonly use:

::

    sudo apt-get update
    sudo apt-get install vim-nox screen elinks

If it has been a while since you created the base VM you may also want to
upgrade the core packages at this point:

::

    sudo apt-get update
    sudo apt-get upgrade -y

At this point you can install the ckan package from within the VM (or on your
local machine if you prefer). When you start the VM, the hostame
``host.buildkit`` is set up to point to the host server. The Apache
configuration for the host server is set up serve the apt repo from the
``host.buildkit`` server alias so the commands below will set up access the
host repo. The ``sudo`` password is ``ubuntu`` by default as already mentioned.
Run the commands now:

::

    sudo apt-get update
    sudo apt-get install -y wget
    echo "deb http://host.buildkit/ckan-1.5 lucid universe" | sudo tee /etc/apt/sources.list.d/okfn.list
    wget -qO- "http://host.buildkit/packages_public.key" | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install -y ckan postgresql-8.4 solr-jetty

.. caution ::

    The last line in the commands above installs CKAN, the PostgreSQL database
    engine, and the Solr search index server. If you intend to connect to a PostgreSQL or
    Solr server that is running on a different machine you don't need to
    install them. In that case, when you run the ``ckan-create-instance`` command later,
    choose ``"no"`` as the third parameter to tell the install command not to
    set up or configure the PostgreSQL database for CKAN. You'll then need to perform any
    database creation and setup steps manually yourself.

If you ever want to upgrade CKAN you can run:

::

    sudo apt-get update
    sudo apt-get upgrade

Sometimes a new CKAN release comes with extra packages. This is considered by
Ubuntu to be a "dist upgrade". In this case run:

::

    sudo apt-get update
    sudo apt-get dist-upgrade

CKAN-specific instructions
--------------------------

In this section we'll look at preciesly how the rest of CKAN is set up. This
serves as a useful example of how you might design your own software to be set
up.

The install will whirr away, downloading over 180Mb of packages (on a clean
install) and take a few minutes, then towards the end you'll see this:

::

    Setting up solr-jetty (1.4.0+ds1-1ubuntu1) ...
     * Not starting jetty - edit /etc/default/jetty and change NO_START to be 0 (or comment it out).

You'll need to configure Solr for use with CKAN. You can do so like this:

::

    sudo ckan-setup-solr

This changes the Solr schema to support CKAN, sets Solr to start automatically
and then starts Solr. You shouldn't be using the Solr instance for anything
apart from CKAN because the command above modifies its schema.

You can now create CKAN instances as you please using the
``ckan-create-instance`` command. It takes these arguments:

Instance name

    This should be a short letter only string representing the name of the CKAN
    instance. It is used (amongst other things) as the basis for:

    * The directory structure of the instance in ``/var/lib/ckan``, ``/var/log/ckan``, ``/etc/ckan`` and elsewhere
    * The name of the PostgreSQL database to use
    * The name of the Solr core to use

Instance Hostname/domain name

    The hostname that this CKAN instance will be hosted at. It is
    used in the Apache configuration virutal host in
    ``/etc/apache2/sites-available/<INSTANCE_NAME>.common`` so that Apache can resolve
    requests directly to CKAN.

    If you install more than one CKAN instance you'll need to set different
    hostnames for each. If you ever want to change the hostname CKAN responds on
    you can do so by editing ``/etc/apache2/sites-available/<INSTANCE_NAME>.common`` and
    restarting apache with ``sudo /etc/init.d/apache2 restart``.

Local PostgreSQL support (``"yes"`` or ``"no"``)

    If you specify ``"yes"``, CKAN will also set up a local database user and
    database and create its tables, populating them as necessary and saving the
    database password in the config file. You would normally say ``"yes"`` unless
    you plan to use CKAN with a PostgreSQL on a remote machine.

For production use the second argument above is usually the domain name of the
CKAN instance, but in our case we are testing, so we'll use the default
hostname buildkit sets up to the server which is ``default.vm.buildkit`` (this
is automatically added to your host machine's ``/etc/hosts`` when the VM is
started so that it will resovle from your host machine - for more complex
setups you'll have to set up DNS entries instead).

Create a new instance like this:

::

    sudo ckan-create-instance std default.vm.buildkit yes

You'll need to specify a new instance name and different hostname for each CKAN
instance you set up.

You can now access your CKAN instance from your host machine as http://default.vm.buildkit/

.. tip ::

    More detailed CKAN instructions are available via the "Package Documentation"
    link at http://pypi.python.org/pypi/ckan/.

Potential Packaging Issues
==========================

There are some gotchas to be aware of with ``buildkit`` so far:

* The packaging process occasionally strips ``__init__.py`` files of all their
  content. It is therefore best to never have information in ``__init__.py``
  files which is why, for extensions, we now have plugins implemented in
  ``plugin.py`` rather than ``__init__.py``.
* Packaging sometimes strips our key directories, such as any named ``dist``,
  they just won't be present in the packaged version.

A future implementation of the packaging may be able to address these
deficiencies. I also have some ideas for other possible future CKAN
enhancements:

* Creating a new instance could also automatically restore from any latest
  dumps that existed for that instance
* When "conflict" functionality is used in the Python packaging, the code is copied
  directly into the main project. At the moment it is the packager's
  responsibility to ensure that the licenses of those conflicting modules are
  copied into the main license for the overall package. It would be nice if the
  packaging code either gave a warning about this or automatically added the
  licenses.

Other ideas:

* Make the buildkit-vm-create command part of the buildkit command
* Swap apt-proxy for something that also caches downoads from virutal machines
  (it currently gives bad header lines which seems to be a known, yet
  unresolved issue) so there is no caching of install packages used in the
  VMs.

More buildkit help
==================

More documentation to come, at the moment you can work out most of what you
need by browsing the online help starting at:

::

    buildkit --help

