#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Pi-Yueh Chuang <pychuang@pm.me>
#
# Distributed under terms of the BSD 3-Clause license.

"""Subparsers & arguments for subcommands
"""
import argparse
from . import subcommands

def _add_docstring(func):
    """Add a docstring to a func and return it.

    All functions in this module have very similar docstring, so we use a
    factory to add docstrings.
    """

    func.__doc__ = \
    """Add arguments of {} command to a subparser.

    Args:
    -----
        subparser_action: a argparse._SubParsersAction (obtained by
            `parser.add_subparsers`).

    Returns:
    --------
        subparser_action: The same object of the input. Returning it just for
            our convenience.
        subparser: the subparser added into the parser.
    """.format(func.__name__)

    return func

@_add_docstring
def show(subparser_action):
    msg = "Show brief information obtained from config file."
    subparser = subparser_action.add_parser("show", description=msg, help=msg)
    subparser.set_defaults(func=subcommands.show)
    return subparser_action, subparser

@_add_docstring
def log(subparser_action):
    msg = "Show Syncthing server's log."
    subparser = subparser_action.add_parser("log", description=msg, help=msg)
    subparser.set_defaults(func=subcommands.log)
    return subparser_action, subparser

@_add_docstring
def scan(subparser_action):
    msg = "Scan a directory/file to triger synchronization."
    subparser = subparser_action.add_parser("scan", description=msg, help=msg)
    subparser.set_defaults(func=subcommands.scan)
    subparser.add_argument("path", action="store", type=str, metavar="PATH", help=msg)
    return subparser_action, subparser

@_add_docstring
def check(subparser_action):
    msg = "Check if the configuration file matches the running server."
    subparser = subparser_action.add_parser("check", description=msg, help=msg)
    subparser.set_defaults(func=subcommands.check)
    return subparser_action, subparser

@_add_docstring
def get(subparser_action):
    msg = "Send a GET request to server. This command is useful for debugging."
    subparser = subparser_action.add_parser("get", description=msg, help=msg)
    subparser.set_defaults(func=subcommands.get)

    subparser.add_argument(
        "endpoint", action="store", type=str, metavar="ENDPOINT",
        help="The GET api endpoint. Options: %(choices)s.",
        choices=subcommands.SyncthingSession._get_apis)

    subparser.add_argument(
        "args", action="store", type=str, metavar="ARGS", nargs=argparse.REMAINDER,
        help="Parameters of the API endpoint.")
    return subparser_action, subparser

@_add_docstring
def post(subparser_action):
    msg = "Send a POST request to server. This command is useful for debugging."
    subparser = subparser_action.add_parser("post", description=msg, help=msg)
    subparser.set_defaults(func=subcommands.post)

    subparser.add_argument(
        "endpoint", action="store", type=str, metavar="ENDPOINT",
        help="The POST api endpoint. Options: %(choices)s.",
        choices=subcommands.SyncthingSession._post_apis)

    subparser.add_argument(
        "args", action="store", type=str, metavar="ARGS", nargs=argparse.REMAINDER,
        help="Parameters of the API endpoint.")
    return subparser_action, subparser
