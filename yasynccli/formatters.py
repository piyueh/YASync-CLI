#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Pi-Yueh Chuang <pychuang@pm.me>
#
# Distributed under terms of the BSD 3-Clause license.

"""Formatters for JSON outputs of different subcommands.
"""
import re

def _add_docstring(func):
    """Add a docstring to a func and return it.

    All functions in this module have very similar docstring, so we use a
    factory to add docstrings.
    """

    func.__doc__ = \
    """Formatter of the output of subcommand `{}`.

    Args:
    -----
        data: a dict (JSON) returned by a HTTP request.

    Returns:
    --------
        A ready to print string.
    """.format(func.__name__)

    return func

@_add_docstring
def log(data):
    s = ""
    for msg in data["messages"]:
        pattern = r"(?P<date>\d{4}-\d{2}-\d{2})T"
        pattern += r"(?P<time>\d{2}:\d{2}:\d{2})\.\d*?"
        pattern += r"(?P<tz>[+-]\d{2}:\d{2})"
        date, time, tz = re.search(pattern, msg["when"]).groups()
        s += "{} {}{}: {}\n".format(date, time, tz, msg["message"])
    return s
