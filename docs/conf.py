# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'django-grpc-framework'
copyright = '2020, Shipeng Feng'
author = 'Shipeng Feng'

# The full version, including alpha/beta/rc tags
import pkg_resources
try:
    release = pkg_resources.get_distribution('djangogrpcframework').version
except pkg_resources.DistributionNotFound:
    print('To build the documentation, the distribution information of')
    print('django-grpc-framework has to be available.  Run "setup.py develop"')
    print('to setup the metadata.  A virtualenv is recommended!')
    sys.exit(1)
del pkg_resources


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

html_theme_options = {
    'github_button': True,
    'github_user': 'fengsp',
    'github_repo': 'django-grpc-framework',
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The master toctree document.
master_doc = 'index'
