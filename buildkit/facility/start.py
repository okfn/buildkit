import base64
import datetime
import os
import sys

templates={
    'setup.py': '''import sys, os
try:
    from setuptools import setup, find_packages
except ImportError:
    print \"You need to install the setuptools module to install this software\"

version = \'%(version)s\'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    \"%(package)s\\n\"
    \"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\\n\\n\"
    \".. contents :: \\n\"
    \"\\n\"+read(\'doc/index.txt\')
    + \'\\n\'
    + read(\'CHANGELOG.txt\')
    + \'\\n\'
    \'License\\n\'
    \'=======\\n\'
    + read(\'LICENSE.txt\')
    + \'\\n\'
    \'Download\\n\'
    \'========\\n\'
)

setup(
    name=\'%(package)s\',
    version=version,
    description=\"%(description)s\",
    long_description=long_description,
    # Get classifiers from http://pypi.python.org/pypi?%%3Aaction=list_classifiers
    classifiers=[
        \'Development Status :: 3 - Alpha\',
        #\'Environment :: Web Environment\',
        \'License :: OSI Approved :: GNU Affero General Public License v3\',
        \'Programming Language :: Python\',
    ],
    keywords=\'\',
    author=\'%(author_name)s\',
    author_email=\'%(author_email)s\',
    url=\'%(url)s\',
    license=\'%(license_name)s\',
    packages=find_packages(exclude=[\'ez_setup\', \'example\', \'test\']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    extras_require={
    },
    entry_points=\"\"\"
    \"\"\",
)
''',
    'LICENSE.txt': '''%(package)s - %(description)s
Copyright (C) %(copyright_years)s %(author_name)s

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

''',
    'setup.cfg': '''[egg_info]
#tag_build = dev
#tag_svn_revision = true
''',
    'MANIFEST.in': '''include doc/index.txt
include doc/source/*.rst
include test/doc.py
include test/README.txt
include example/*.py
include example/README.txt
include ez_setup.py
include CHANGELOG.txt
include LICENSE.txt

recursive_include *_deb *
''',
    'CHANGELOG.txt': '''Changes
=======

0.1.0
-----

%(changelog_date)s
~~~~~~~~~~

* Created package

''',
    'README.txt': '''See ``doc/index.txt`` for information.
''',
    'requires/lucid_missing.txt': '''# These are packages that we rely on that aren\'t present in Lucid. We package
# them and put them in our own CKAN repository
#
# Note:
#
#     Developers, our build script for the Debian packages relies on the 
#     requirements above being specified as editable resources with their
#     mercurial, SVN or git repository specified at the correct revision to
#     package
#
# Here are some examples (note that we put the equivalent requirement in a
# comment):
# 
#     # pyutilib.component.core>=4.1,<4.1.99
#     -e svn+https://software.sandia.gov/svn/public/pyutilib/pyutilib.component.core/trunk@1972#egg=pyutilib.component.core
#     # licenses==0.4,<0.6.99
#     -e hg+https://bitbucket.org/okfn/licenses@0eed4a13296b#egg=licenses
#     # vdm>=0.9,<0.9.99
#     -e hg+https://bitbucket.org/okfn/vdm@vdm-0.9#egg=vdm
#     # markupsafe==0.9.2 required by webhelpers==1.2 required by formalchemy with SQLAlchemy 0.6
#     -e git+https://github.com/mitsuhiko/markupsafe.git@0.9.2#egg=markupsafe
#     # autoneg>=0.5
#     -e git+https://github.com/wwaites/autoneg.git@b4c727b164f411cc9d60#egg=autoneg
#     # flup>=0.5
#     -e hg+http://hg.saddi.com/flup@301a58656bfb#egg=flup
#     # All the conflicting dependencies from the lucid_conflict.txt file
#     -e hg+https://bitbucket.org/okfn/ckan-deps@6287665a1965#egg=ckan-deps
#     # FormAlchemy
#     -e git+https://github.com/FormAlchemy/formalchemy.git@1.3.9#egg=formalchemy

# Put your entries here...

''',
    'requires/lucid_present.txt': '''# These are dependencies that are already in Lucid and should be installed via
# apt-get if you are on that platform. If you are using a different platform
# you can install these dependencies via pip instead.
#
# Note:
#
#     Developers, please do not edit the versions, these versions are fixed
#     in Lucid. If you start to depend on a different vesion you\'ll need to
#     remove the version here and package your version as a conflict.
#
# Here are some examples:
#
#     babel==0.9.4
#     psycopg2==2.0.13
#     lxml==2.2.4
#     sphinx==0.6.4
#     # Specifying particular version of WebOb because later version has incompatibility
#     # with pylons 0.9.7 (change to imports of Multidict)
#     webob==1.0.8
#     Pylons==0.9.7
#     repoze.who==1.0.18
#     tempita==0.4
#     zope.interface==3.5.3
#     # These are both combined into the python-repoze.who-plugins package
#     repoze.who.plugins.openid
#     # Actually from python-repoze.who-plugins but the openid plugin in the same
#     # package is too old
#     repoze.who-friendlyform==1.0.8
#     routes==1.11
#     paste==1.7.2
#     pastescript==1.7.3

# Put your entries here...
''',
    'requires/lucid_conflict.txt': '''# These are packages where we require a different version of a package from
# the one in Lucid. Rather than packaging a backport which could potentially
# interfere with a user\'s other installed software, we put these modules into
# a single location which is imported from in preference to the Lucid 
# equivalent.
#
# Note:
#
#     Developers, our build script for the Debian packages relies on the 
#     requirements above being specified as editable resources with their
#     mercurial, SVN or git repository specified at the correct revision to
#     package.
# 
# Here are some examples (note that we put the equivalent requirement in a
# comment):
# 
#     # pyutilib.component.core>=4.1,<4.1.99
#     -e svn+https://software.sandia.gov/svn/public/pyutilib/pyutilib.component.core/trunk@1972#egg=pyutilib.component.core
#     # licenses==0.4,<0.6.99
#     -e hg+https://bitbucket.org/okfn/licenses@0eed4a13296b#egg=licenses
#     # vdm>=0.9,<0.9.99
#     -e hg+https://bitbucket.org/okfn/vdm@vdm-0.9#egg=vdm
#     # markupsafe==0.9.2 required by webhelpers==1.2 required by formalchemy with SQLAlchemy 0.6
#     -e git+https://github.com/mitsuhiko/markupsafe.git@0.9.2#egg=markupsafe
#     # autoneg>=0.5
#     -e git+https://github.com/wwaites/autoneg.git@b4c727b164f411cc9d60#egg=autoneg
#     # flup>=0.5
#     -e hg+http://hg.saddi.com/flup@301a58656bfb#egg=flup
#     # All the conflicting dependencies from the lucid_conflict.txt file
#     -e hg+https://bitbucket.org/okfn/ckan-deps@6287665a1965#egg=ckan-deps
#     # FormAlchemy
#     -e git+https://github.com/FormAlchemy/formalchemy.git@1.3.9#egg=formalchemy

# Put your entries here...

''',
    'distro/lucid/debian/control.template': '''Package: %(distro_package)s
# These variables are overwritten by the build system so should not be 
# completed...
# Version: 
Maintainer: %(author_name)s <%(author_email)s>
Installed-Size: 0
Pre-Depends: %(distro_pre_depends)s
Depends: %(distro_depends)s
Section: %(distro_section)s
Priority: extra
XS-Python-Version: >= 2.5
Architecture: all
Homepage: %(url)s
Description: %(distro_package)s
 %(description)s
''',
    'buildkit/__init__.py': '''''',
    'test/doc.py': '''\"\"\"\\
Doctests for %(package)s
\"\"\"
import doctest
import logging
logging.basicConfig(level=logging.DEBUG)

import sys; sys.path.append(\'../\')

doctest.testfile(\'../doc/source/manual.rst\', optionflags=doctest.ELLIPSIS)
doctest.testfile(\'../doc/source/api.rst\', optionflags=doctest.ELLIPSIS)
''',
    'test/README.txt': '''Tests go in this directory
''',
    'example/README.txt': '''``build.py``
    Build a set of packages laid out in the directory structure described in
    the manual

``new_package.py``
    Create a new package (you\'ll need to move all the files within it to a
    ``trunk`` directory for it to be compatible with %(package)s but this is
    handled by ``package_to_repo.py``)

``package_to_repo.py``
    Turn a package created by ``new_package.py`` into a mercurial repository
    capable of being handled by %(package)s and the ``build.py`` script.
''',
    'doc/Makefile': '''# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = ~/env/bin/sphinx-build
PAPER         =
BUILDDIR      = build

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) source

.PHONY: help clean html dirhtml pickle json htmlhelp qthelp latex changes linkcheck doctest

help:
	@echo \"Please use `make <target>\' where <target> is one of\"
	@echo \"  html      to make standalone HTML files\"
	@echo \"  dirhtml   to make HTML files named index.html in directories\"
	@echo \"  pickle    to make pickle files\"
	@echo \"  json      to make JSON files\"
	@echo \"  htmlhelp  to make HTML files and a HTML help project\"
	@echo \"  qthelp    to make HTML files and a qthelp project\"
	@echo \"  latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter\"
	@echo \"  changes   to make an overview of all changed/added/deprecated items\"
	@echo \"  linkcheck to check all external links for integrity\"
	@echo \"  doctest   to run all doctests embedded in the documentation (if enabled)\"

clean:
	-rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo \"Build finished. The HTML pages are in $(BUILDDIR)/html.\"

dirhtml:
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo \"Build finished. The HTML pages are in $(BUILDDIR)/dirhtml.\"

pickle:
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
	@echo
	@echo \"Build finished; now you can process the pickle files.\"

json:
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo
	@echo \"Build finished; now you can process the JSON files.\"

htmlhelp:
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo
	@echo \"Build finished; now you can run HTML Help Workshop with the\" \\
	      \".hhp project file in $(BUILDDIR)/htmlhelp.\"

qthelp:
	$(SPHINXBUILD) -b qthelp $(ALLSPHINXOPTS) $(BUILDDIR)/qthelp
	@echo
	@echo \"Build finished; now you can run \"qcollectiongenerator\" with the\" \\
	      \".qhcp project file in $(BUILDDIR)/qthelp, like this:\"
	@echo \"# qcollectiongenerator $(BUILDDIR)/qthelp/PermissionKit.qhcp\"
	@echo \"To view the help file:\"
	@echo \"# assistant -collectionFile $(BUILDDIR)/qthelp/PermissionKit.qhc\"

latex:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo
	@echo \"Build finished; the LaTeX files are in $(BUILDDIR)/latex.\"
	@echo \"Run `make all-pdf\' or `make all-ps\' in that directory to\" \\
	      \"run these through (pdf)latex.\"

changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo \"The overview file is in $(BUILDDIR)/changes.\"

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo \"Link check complete; look for any errors in the above output \" \\
	      \"or in $(BUILDDIR)/linkcheck/output.txt.\"

doctest:
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo \"Testing of doctests in the sources finished, look at the \" \\
	      \"results in $(BUILDDIR)/doctest/output.txt.\"
''',
    'doc/index.txt': '''Summary
=======

%(description)s

Get Started
===========

* Download and install from source

Author
======

`%(author_name)s <%(author_url)s>`_
''',
    'doc/source/index.rst': '''%(version)s
+++++

.. include :: ../index.txt

Documentation
=============

.. toctree::
   :maxdepth: 2

   manual
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
''',
    'doc/source/conf.py': '''# -*- coding: utf-8 -*-
#
# %(package)s documentation build configuration file, based on 
# sphinx-quickstart created in %(copyright_years)s.
#  
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.append(os.path.abspath(\'.\'))

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named \'sphinx.ext.*\') or your custom ones.
extensions = [\'sphinx.ext.autodoc\', \'sphinx.ext.doctest\']

# Add any paths that contain templates here, relative to this directory.
templates_path = [\'_templates\']

# The suffix of source filenames.
source_suffix = \'.rst\'

# The encoding of source files.
#source_encoding = \'utf-8\'

# The master toctree document.
master_doc = \'index\'

# General information about the project.
project = u\'%(package)s\'
copyright = u\'%(copyright_years)s, %(author_name)s\'

# The version info for the project you\'re documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = \'%(version)s\'
# The full version, including alpha/beta/rc tags.
release = \'%(version)s\'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = \'\'
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = \'%%B %%d, %%Y\'

# List of documents that shouldn\'t be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn\'t be searched
# for source files.
exclude_trees = []

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, \'()\' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = \'sphinx\'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently \'default\' and \'sphinxdoc\'.
html_theme = \'dwt_jimmyg\'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# \"<project> v<release> documentation\".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named \"default.css\" will overwrite the builtin \"default.css\".
html_static_path = [\'_static\']

# If not \'\', a \'Last updated on:\' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = \'%%b %%d, %%Y\'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_use_modindex = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = \'\'
# If nonempty, this is the file name suffix for HTML files (e.g. \".xhtml\").
#html_file_suffix = \'\'

# Output file base name for HTML help builder.
htmlhelp_basename = \'\'


# -- Options for LaTeX output --------------------------------------------------

# The paper size (\'letter\' or \'a4\').
#latex_paper_size = \'letter\'

# The font size (\'10pt\', \'11pt\' or \'12pt\').
#latex_font_size = \'10pt\'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  (\'index\', \'%(package)s.tex\', u\'%(package)s Documentation\',
   u\'%(author_name)s\', \'manual\'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For \"manual\" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = \'\'

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True
''',
    'doc/source/manual.rst': '''Manual
++++++

To write.
''',
    'doc/source/api.rst': '''API Documentation
+++++++++++++++++
   
.. automodule:: %(module)s 
   :members:
   :undoc-members:
''',
}

def generate(
    start,
    replacements, 
    base_path=None
):
    for k in ['version', 'module', 'description']:
        if not replacements.get(k):
            raise Exception('No %s specified'%k)
    template_vars = {
        'copyright_years': str(datetime.datetime.now().year),
        'changelog_date': datetime.datetime.now().strftime('YYYY-mm-dd'),
        'author_url': '',
        'distro_depends': '', 
        'distro_package': replacements['module'], 
        'package': replacements['module'], 
        'distro_section': 'main/web', 
        'distro_pre_depends': '', 
        'license_name': '', 
        'url': '', 
        'author_email': '',
        'author_name': '',
    }
    template_vars.update(replacements)
    if base_path is None:
        base_path = os.getcwd()
    elif not os.path.exists(base_path):
        os.mkdir(base_path)
    if os.path.exists(os.path.join(base_path, "require"%dict(template_vars))):
        raise Exception("Directory already exists: %s" % (os.path.join(base_path, "require"%dict(template_vars))))
    os.mkdir(os.path.join(base_path, "require"%dict(template_vars)))
    if os.path.exists(os.path.join(base_path, "distro"%dict(template_vars))):
        raise Exception("Directory already exists: %s" % (os.path.join(base_path, "distro"%dict(template_vars))))
    os.mkdir(os.path.join(base_path, "distro"%dict(template_vars)))
    if os.path.exists(os.path.join(base_path, "%(module)s"%dict(template_vars))):
        raise Exception("Directory already exists: %s" % (os.path.join(base_path, "%(module)s"%dict(template_vars))))
    os.mkdir(os.path.join(base_path, "%(module)s"%dict(template_vars)))
    if os.path.exists(os.path.join(base_path, "test"%dict(template_vars))):
        raise Exception("Directory already exists: %s" % (os.path.join(base_path, "test"%dict(template_vars))))
    os.mkdir(os.path.join(base_path, "test"%dict(template_vars)))
    if os.path.exists(os.path.join(base_path, "example"%dict(template_vars))):
        raise Exception("Directory already exists: %s" % (os.path.join(base_path, "example"%dict(template_vars))))
    os.mkdir(os.path.join(base_path, "example"%dict(template_vars)))
    if os.path.exists(os.path.join(base_path, "doc"%dict(template_vars))):
        raise Exception("Directory already exists: %s" % (os.path.join(base_path, "doc"%dict(template_vars))))
    os.mkdir(os.path.join(base_path, "doc"%dict(template_vars)))
    if os.path.exists(os.path.join(base_path, "requires"%dict(template_vars))):
        raise Exception("Directory already exists: %s" % (os.path.join(base_path, "requires"%dict(template_vars))))
    os.mkdir(os.path.join(base_path, "requires"%dict(template_vars)))
    if os.path.exists(os.path.join(base_path, "distro/lucid"%dict(template_vars))):
        raise Exception("Directory already exists: %s" % (os.path.join(base_path, "distro/lucid"%dict(template_vars))))
    os.mkdir(os.path.join(base_path, "distro/lucid"%dict(template_vars)))
    if os.path.exists(os.path.join(base_path, "distro/lucid/debian"%dict(template_vars))):
        raise Exception("Directory already exists: %s" % (os.path.join(base_path, "distro/lucid/debian"%dict(template_vars))))
    os.mkdir(os.path.join(base_path, "distro/lucid/debian"%dict(template_vars)))
    if os.path.exists(os.path.join(base_path, "doc/source"%dict(template_vars))):
        raise Exception("Directory already exists: %s" % (os.path.join(base_path, "doc/source"%dict(template_vars))))
    os.mkdir(os.path.join(base_path, "doc/source"%dict(template_vars)))
    if os.path.exists(os.path.join(base_path, 'setup.py'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'setup.py'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'setup.py'%dict(template_vars)), 'wb')
    fp.write(templates['setup.py']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'LICENSE.txt'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'LICENSE.txt'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'LICENSE.txt'%dict(template_vars)), 'wb')
    fp.write(templates['LICENSE.txt']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'setup.cfg'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'setup.cfg'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'setup.cfg'%dict(template_vars)), 'wb')
    fp.write(templates['setup.cfg']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'MANIFEST.in'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'MANIFEST.in'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'MANIFEST.in'%dict(template_vars)), 'wb')
    fp.write(templates['MANIFEST.in']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'CHANGELOG.txt'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'CHANGELOG.txt'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'CHANGELOG.txt'%dict(template_vars)), 'wb')
    fp.write(templates['CHANGELOG.txt']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'README.txt'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'README.txt'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'README.txt'%dict(template_vars)), 'wb')
    fp.write(templates['README.txt']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'requires/lucid_missing.txt'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'requires/lucid_missing.txt'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'requires/lucid_missing.txt'%dict(template_vars)), 'wb')
    fp.write(templates['requires/lucid_missing.txt']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'requires/lucid_present.txt'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'requires/lucid_present.txt'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'requires/lucid_present.txt'%dict(template_vars)), 'wb')
    fp.write(templates['requires/lucid_present.txt']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'requires/lucid_conflict.txt'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'requires/lucid_conflict.txt'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'requires/lucid_conflict.txt'%dict(template_vars)), 'wb')
    fp.write(templates['requires/lucid_conflict.txt']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'distro/lucid/debian/control.template'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'distro/lucid/debian/control.template'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'distro/lucid/debian/control.template'%dict(template_vars)), 'wb')
    fp.write(templates['distro/lucid/debian/control.template']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, '%(module)s/__init__.py'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, '%(module)s/__init__.py'%dict(template_vars)))
    fp = open(os.path.join(base_path, '%(module)s/__init__.py'%dict(template_vars)), 'wb')
    fp.write(templates['buildkit/__init__.py']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'test/doc.py'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'test/doc.py'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'test/doc.py'%dict(template_vars)), 'wb')
    fp.write(templates['test/doc.py']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'test/README.txt'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'test/README.txt'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'test/README.txt'%dict(template_vars)), 'wb')
    fp.write(templates['test/README.txt']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'example/README.txt'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'example/README.txt'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'example/README.txt'%dict(template_vars)), 'wb')
    fp.write(templates['example/README.txt']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'doc/Makefile'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'doc/Makefile'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'doc/Makefile'%dict(template_vars)), 'wb')
    fp.write(templates['doc/Makefile']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'doc/index.txt'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'doc/index.txt'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'doc/index.txt'%dict(template_vars)), 'wb')
    fp.write(templates['doc/index.txt']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'doc/source/index.rst'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'doc/source/index.rst'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'doc/source/index.rst'%dict(template_vars)), 'wb')
    fp.write(templates['doc/source/index.rst']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'doc/source/conf.py'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'doc/source/conf.py'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'doc/source/conf.py'%dict(template_vars)), 'wb')
    fp.write(templates['doc/source/conf.py']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'doc/source/manual.rst'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'doc/source/manual.rst'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'doc/source/manual.rst'%dict(template_vars)), 'wb')
    fp.write(templates['doc/source/manual.rst']%dict(template_vars))
    fp.close()
    if os.path.exists(os.path.join(base_path, 'doc/source/api.rst'%dict(template_vars))):
        raise Exception('File already exists: %s' % os.path.join(base_path, 'doc/source/api.rst'%dict(template_vars)))
    fp = open(os.path.join(base_path, 'doc/source/api.rst'%dict(template_vars)), 'wb')
    fp.write(templates['doc/source/api.rst']%dict(template_vars))
    fp.close()
    return template_vars

if __name__ == "__main__" and len(sys.argv)>1 and not os.path.exists(sys.argv[1]):
    print "Creating tempalate..."
    render(base_path=sys.argv[1])
