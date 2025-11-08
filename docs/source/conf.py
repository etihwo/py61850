import os

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "py61850"
copyright = "2025, etihwo"
author = "etihwo"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    # "myst_parser",
    "myst_nb",
    "sphinx_copybutton",
]


templates_path = ["_templates"]
exclude_patterns = ["Thumbs.db", ".DS_Store", "conf.py"]
# source_suffix = {
#     # ".md": "myst-nb",
#     # ".py": "myst-nb",
#     ".ipynb": "myst-nb",
# }

# nb_custom_formats = {".py": ["jupytext.reads", {"fmt": "py:percent"}]}
nb_custom_formats = {".py": ["jupytext.reads", {"fmt": "py:light"}]}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]

# Napoleon settings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# autodoc configuration
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
}

# Auto summary
autosummary_ignore_module_all = False

# myst_parser configuration
myst_enable_extensions = [
    "colon_fence",
]

# Sphinx-gallery
sphinx_gallery_conf = {
    "examples_dirs": os.path.join("..", "..", "examples"),  # path to your example scripts
    "gallery_dirs": "auto_examples",  # path to where to save gallery generated output
    "show_memory": False,
    "reference_url": {
        # The module you locally document uses None
        "sphinx_gallery": None,
    },
    "download_all_examples": False,
}

# myst_nb configuration
nb_execution_mode = "off"
