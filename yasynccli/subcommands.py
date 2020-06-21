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
from .session import SyncthingSession

def show(args):
    """Subcommand show.

    Args:
    -----
        args: resulting namespace from parsing CMD arguments.
    """

    print(SyncthingSession(args.config, args.url, args.apikey))

def get(args):
    """Subcommand get.

    Args:
    -----
        args: resulting namespace from parsing CMD arguments.
    """

    params = {}
    for s in args.args:
        match = re.search(r"^(?P<key>.+?)=(?P<value>.+?)$", s)
        params[match.group("key")] = match.group("value")

    pprint.pprint(SyncthingSession(args.config, args.url, args.apikey).get(
        args.endpoint, timeout=5, params=params).json())

def post(args):
    """Subcommand post.

    Args:
    -----
        args: resulting namespace from parsing CMD arguments.
    """

    params = {}
    for s in args.args:
        match = re.search(r"^(?P<key>.+?)=(?P<value>.+?)$", s)
        params[match.group("key")] = match.group("value")

    response = SyncthingSession(args.config, args.url, args.apikey).post(
        args.endpoint, timeout=5, params=params)
    response.raise_for_status()
