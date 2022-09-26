#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# PennyLane-AQT documentation build configuration file.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.
import sys, os, re

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('_ext'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath('.')), 'doc'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.6'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.intersphinx",
    'sphinx.ext.viewcode',
    "sphinx_automodapi.automodapi",
    'sphinx_automodapi.smart_resolver'
]

intersphinx_mapping = {"https://docs.pennylane.ai/en/stable/": None}

autosummary_generate = True
autosummary_imported_members = False
automodapi_toctreedirnm = "code/api"
automodsumm_inherited_members = True

# Add any paths that contain templates here, relative to this directory.
from pennylane_sphinx_theme import templates_dir
templates_path = [templates_dir()]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'PennyLane-AQT'
copyright = "2022, Xanadu Quantum Technologies Inc."
author = 'Xanadu Inc.'

add_module_names = False

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

import pennylane_aqt
# The full version, including alpha/beta/rc tags.
release = pennylane_aqt.__version__

# The short X.Y version.
version = re.match(r'^(\d+\.\d+)', release).expand(r'\1')

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# today_fmt is used as the format for a strftime call.
today_fmt = '%Y-%m-%d'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars


# -- Xanadu theme ---------------------------------------------------------
html_theme = 'pennylane'

# xanadu theme options (see theme.conf for more information)
html_theme_options = {
    "navbar_name": "PennyLane-AQT",
    "extra_copyrights": [
        "TensorFlow, the TensorFlow logo, and any related marks are trademarks "
        "of Google Inc."
    ],
    "toc_overview": True,
    "navbar_active_link": 3,
    "google_analytics_tracking_id": "UA-130507810-1"
}

edit_on_github_project = 'PennyLaneAI/pennylane-aqt'
edit_on_github_branch = 'master/doc'

#============================================================

# the order in which autodoc lists the documented members
autodoc_member_order = 'bysource'

# inheritance_diagram graphviz attributes
inheritance_node_attrs = dict(color='lightskyblue1', style='filled')

#autodoc_default_flags = ['members']
autosummary_generate = True
