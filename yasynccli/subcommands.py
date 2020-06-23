#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Pi-Yueh Chuang <pychuang@pm.me>
#
# Distributed under terms of the BSD 3-Clause license.

"""Subcommand wrappers.
"""
import sys
import re
import pprint
import pathlib
import logging
import requests
from .session import SyncthingSession
from . import formatters

# get a logger with dummy handler if the caller does not have logging config
logger = logging.getLogger("yasynccli.subcommands")
logger.addHandler(logging.NullHandler())

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
    logger.debug("Starting subcommand `{}`.".format("log"))
    syncthing = SyncthingSession(args.config, args.url, args.apikey)
    result = syncthing.get("system", "log", timeout=60)
    result.raise_for_status()
    string = formatters.log(result.json())
    logger.debug("Done subcommand `{}`.".format("log"))
    print(string)

@_add_docstring
def scan(args):
    logger.debug("Starting subcommand `{}`.".format("scan"))

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
    logger.debug("Done subcommand `{}`.".format("scan"))

@_add_docstring
def check(args):
    logger.debug("Starting subcommand `{}`.".format("check"))
    syncthing = SyncthingSession(args.config, args.url, args.apikey)

    try:
        response = syncthing.get("system", "config", timeout=60)
        response.raise_for_status()

    # server connection error
    except requests.exceptions.ConnectionError:
        sys.stderr.write("Error: couldn't connect to server at {}\n".format(syncthing.url))
        sys.exit(1)

    # server connected, but forbided our client
    except requests.exceptions.HTTPError:
        sys.stderr.write("Error: server refused the clint. Maybe check the API key?\n")
        sys.exit(1)

    config = response.json()
    config["instance"] = syncthing # because formatters.check only takes one arg
    formatters.check(config)

    logger.debug("Done subcommand `{}`.".format("check"))

@_add_docstring
def get(args):
    logger.debug("Starting subcommand `{}`.".format("get"))

    params = {}
    for s in args.args:
        match = re.search(r"^(?P<key>.+?)=(?P<value>.+?)$", s)
        params[match.group("key")] = match.group("value")

    response = SyncthingSession(args.config, args.url, args.apikey).get(
        args.endpoint, timeout=60, params=params)
    response.raise_for_status()

    logger.debug("Done subcommand `{}`.".format("get"))
    pprint.pprint(response.json())

@_add_docstring
def post(args):
    logger.debug("Starting subcommand `{}`.".format("post"))

    params = {}
    for s in args.args:
        match = re.search(r"^(?P<key>.+?)=(?P<value>.+?)$", s)
        params[match.group("key")] = match.group("value")

    response = SyncthingSession(args.config, args.url, args.apikey).post(
        args.endpoint, timeout=60, params=params)
    response.raise_for_status()
    logger.debug("Done subcommand `{}`.".format("post"))
