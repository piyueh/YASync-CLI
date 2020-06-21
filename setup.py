#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Pi-Yueh Chuang <pychuang@pm.me>
#
# Distributed under terms of the BSD 3-Clause license.

"""Setup script.
"""
import setuptools

def get_strings():
    """Get content of __version__, description, and README.

    Note for __version__:
        It's is not recommended to get __version__ by importing the package
        because it may cause problems if __init__.py imports packages that will
        be listed in install_requires of setuptools.setup. So instead, it is
        recommended to use string parsing to obtain the version.

    For description, it's just convenient to mantain such string at a single
    place.

    Args:
    -----
        None.

    Returns:
    --------
        version: a str: the version string.
        desc: a str: one line description summarizing the package.
        readme: a str; the content of README.md.
    """
    import re
    import pathlib

    # the absolute path to the root directory
    rootdir = pathlib.Path(__file__).resolve().parent

    # read README.md and overwrite readme
    with open(rootdir.joinpath("README.md"), 'r') as f:
        readme = f.read()

    # read __init__.py
    with open(rootdir.joinpath("yasynccli", "__init__.py"), 'r') as f:
        content = f.read()

    # version
    version = re.search("__version__\s*?=\s*?(?P<version>\S+?)$", content, re.MULTILINE)
    version = version.group("version").strip("\"\'")

    # desc
    desc = re.search("^\"\"\"(?P<desc>\S.*?)$", content, re.MULTILINE)
    desc = desc.group("desc")

    return version, desc, readme

meta = dict(
    name="yasynccli",
    long_description_content_type="text/markdown",
    author="Pi-Yueh Chuang",
    author_email="pychuang@pm.me",
    url="https://github.com/piyueh/yasynccli",
    packages=setuptools.find_packages(),
    keywords=["Syncthing", "syncthing"],
    license="BSD 3-Clause License",
    include_package_data=True,
    entry_points={"console_scripts": ["yasync-cli = yasynccli.__main__:main"]},
    tests_require=["pytest"],
)

# info from __init__.py
meta["version"], meta["description"], meta["long_description"] = get_strings()

# classifiers for categorizing
meta["classifiers"] = [
    "Development Status :: 1 - Planning"
    "Environment :: Console",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Utilities"
]

if __name__ == "__main__":
    setuptools.setup(**meta)
