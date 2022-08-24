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
templates_path = ['_templates', 'xanadu_theme']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'PennyLane-AQT'
copyright = "Copyright 2020"
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
html_theme = 'xanadu'

html_sidebars = {
    '**': [
        'searchbox.html',
        'globaltoc.html',
    ]
}

# xanadu theme options (see theme.conf for more information)
html_theme_options = {
    "navbar_logo_path": "_static/logo.png",
    "navbar_wordmark_path": "_static/pennylane.svg",
    # Specifying #19b37b is more correct but does not match the other PL websites.

    "navbar_logo_colour": "#2d7c7f",

    "navbar_home_link": "https://pennylane.ai",

    "navbar_left_links": [
        {
            "name": "Quantum machine learning",
            "href": "https://pennylane.ai/qml/",
        },
        {
            "name": "Demos",
            "href": "https://pennylane.ai/qml/demonstrations.html",
        },
        {
            "name": "Install",
            "href": "https://pennylane.ai/install.html",
        },
        {
            "name": "Plugins",
            "href": "https://pennylane.ai/plugins.html",
            "active": True,
        },
        {
            "name": "Documentation",
            "href": "https://docs.pennylane.ai/",
        },
        {
            "name": "Blog",
            "href": "https://pennylane.ai/blog/",
        }
    ],

    "navbar_right_links": [
        {
            "name": "FAQ",
            "href": "https://pennylane.ai/faq.html",
            "icon": "fas fa-question",
        },
        {
            "name": "Support",
            "href": "https://discuss.pennylane.ai/",
            "icon": "fab fa-discourse",
        },
        {
            "name": "GitHub",
            "href": "https://github.com/PennyLaneAI/pennylane-qiskit",
            "icon": "fab fa-github",
        }
    ],

    "extra_copyrights": [
        "TensorFlow, the TensorFlow logo, and any related marks are trademarks "
        "of Google Inc."
    ],
    "google_analytics_tracking_id": "UA-130507810-1",
    "border_colour": "#19b37b",
    "prev_next_button_colour": "#19b37b",
    "prev_next_button_hover_colour": "#0e714d",
    "table_header_background_colour": "#edf7f4",
    "text_accent_colour": "#19b37b",
    "toc_marker_colour": "#19b37b",
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

from directives import CustomDeviceGalleryItemDirective

def setup(app):
    app.add_directive('devicegalleryitem', CustomDeviceGalleryItemDirective)

