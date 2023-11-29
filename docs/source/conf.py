import os
import sys
sys.path.insert(0, os.path.abspath('./../..'))

# -- Project information -----------------------------------------------------

import sebaubuntu_libs

project = 'sebaubuntu_libs'
copyright = '2022, Sebastiano Barezzi'
author = 'Sebastiano Barezzi'
release = sebaubuntu_libs.__version__

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.duration',
    'sphinx.ext.intersphinx',
]

autosummary_generate = True

add_function_parentheses = True

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

intersphinx_disabled_domains = ['std']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

# -- Setup function ----------------------------------------------------------

import types

def setup(app):
    app.connect('autodoc-skip-member', special_methods_callback)

def special_methods_callback(app, what, name, obj, skip, options):
    """
    https://stackoverflow.com/questions/5599254/how-to-use-sphinxs-autodoc-to-document-a-classs-init-self-method/35493334#35493334
    """
    if getattr(obj, '__doc__', None) and isinstance(obj, (types.FunctionType, types.MethodType)):
        return False
    else:
        return skip
