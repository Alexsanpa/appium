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
import os
import sys
import sphinx_theme
from pathlib import Path

sys.path.insert(0, os.path.abspath('../'))


# -- Project information -----------------------------------------------------

project = 'Sapyautomation'
copyright = '2020, Deloitte'
author = 'Francisco Prieto'
# The full version, including alpha/beta/rc tags
version = '0.1.0'
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.todo',
    'sphinx.ext.napoleon'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

req_path = Path.cwd().parent.joinpath('requirements.txt')

autodoc_mock_imports = ['win32com', 'webdriver_manager', 'pyautogui', 'cv2',
                        'HtmlTestRunner', ]

with req_path.open('r') as f:
    for line in f.readlines():
        autodoc_mock_imports.append(line.split('==')[0])

# -- Options for HTML output -------------------------------------------------

# Napoleon settings
napoleon_numpy_docstring = False
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True

# ---sphinx-themes-----

html_theme_options = {
    'collapse_navigation': True,
    'display_version': True,
    'navigation_depth': 3,
}
html_theme = "neo_rtd_theme"
html_theme_path = [sphinx_theme.get_html_theme_path('stanford-theme')]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
