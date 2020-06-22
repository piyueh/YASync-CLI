#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Pi-Yueh Chuang <pychuang@pm.me>
#
# Distributed under terms of the BSD 3-Clause license.

"""Subcommand wrappers.
"""
import re
import pprint
import pathlib
from .session import SyncthingSession
from . import formatters

def _add_docstring(func):
    """Add a docstring to a func and return it.

    All functions in this module have very similar docstring, so we use a
    factory to add docstrings.
    """

    func.__doc__ = \
    """Entry of subcommand `{}`.

    Args:
    -----
        args: resulting namespace from parsing CMD arguments.
    """.format(func.__name__)

    return func

@_add_docstring
def show(args):
    print(SyncthingSession(args.config, args.url, args.apikey))

@_add_docstring
def log(args):
    syncthing = SyncthingSession(args.config, args.url, args.apikey)
    result = syncthing.get("system", "log", timeout=60).json()
    string = formatters.log(result)
    print(string)

@_add_docstring
def get(args):

    params = {}
    for s in args.args:
        match = re.search(r"^(?P<key>.+?)=(?P<value>.+?)$", s)
        params[match.group("key")] = match.group("value")

    pprint.pprint(SyncthingSession(args.config, args.url, args.apikey).get(
        args.endpoint, timeout=60, params=params).json())

@_add_docstring
def post(args):

    params = {}
    for s in args.args:
        match = re.search(r"^(?P<key>.+?)=(?P<value>.+?)$", s)
        params[match.group("key")] = match.group("value")

    response = SyncthingSession(args.config, args.url, args.apikey).post(
        args.endpoint, timeout=60, params=params)
    response.raise_for_status()

@_add_docstring
def scan(args):

    params = dict(folder=None, sub=None)

    # convert to full & absolute path & check existence
    target = pathlib.Path(args.path).expanduser().resolve()
    if not target.exists():
        raise FileNotFoundError("{} not found".format(target))

    syncthing = SyncthingSession(args.config, args.url, args.apikey)

    # naive way to find monitored folder and relative path
    for p, values in syncthing.folders.items():

        # only if target is under/equals to p then no exception is raised
        try:
            sub = target.relative_to(p)
        except ValueError:
            continue

        params["folder"] = values["id"]
        params["sub"] = None if sub == pathlib.Path('.') else str(sub)
        break

    if params["folder"] is None:
        raise ValueError("{} does not belong to any monitored folder.".format(target))

    response = syncthing.post("db", "scan", timeout=60, params=params)
    response.raise_for_status()
