#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2020 Pi-Yueh Chuang <pychuang@pm.me>
#
# Distributed under terms of the BSD 3-Clause license.

"""Main function/script of YASync-CLI.
"""
import logging
import argparse
import pathlib
import textwrap
from . import __version__
from . import arguments

def get_parser():
    """Get an argparse.ArgumentParser with arguments.

    Returns:
    --------
        A ready-to-use `argparse.ArgumentParser`.
    """

    description = \
        "Yet Another Syncthing CLI Tool." + \
        "\n\n" + \
        "Use `yasync-cli <COMMAND> -h` to see the help of each sub-command." + \
        "\n\n" + \
        textwrap.fill(
            "yasync-cli is a command-line tool to communicate with a Syncthing "
            "daemon from a terminal. It is supposed to be useful for headless "
            "servers.", width=80)

    epilog = "Released under BSD 3-Clause License.\n" +\
        "Website: https://github.com/piyueh/YASync-CLI"

    parser = argparse.ArgumentParser(
        "yasync-cli", formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description, epilog=epilog)

    # version
    parser.add_argument(
        "--version", action='version', version='%(prog)s {}'.format(__version__))

    # logger
    helpmsg = "log level. Options: %(choices)s (Default: %(default)s)"
    parser.add_argument(
        "--log-level", action="store", default=None, type=str,
        choices=["debug", "info", "warning", "error", "critical"],
        help=helpmsg, metavar="LEVEL", dest="log_level")

    helpmsg = "log file path (Default: %(default)s)"
    parser.add_argument(
        "--log-file", action="store", default=None, type=pathlib.Path,
        help=helpmsg, metavar="FILE", dest="log_file")

    # alternative configuration file, url, and api key
    helpmsg = "alternative configuration file (Default: %(default)s)"
    parser.add_argument(
        "--config", action="store", type=pathlib.Path,
        default=pathlib.Path("~").joinpath(".config", "syncthing", "config.xml"),
        help=helpmsg, metavar="CONFIG", dest="config")

    helpmsg = "alternative URL (Default: %(default)s)"
    parser.add_argument(
        "--url", action="store", type=str, default="From config file",
        help=helpmsg, metavar="URL", dest="url")

    helpmsg = "alternative API key (Default: %(default)s)"
    parser.add_argument(
        "--api-key", action="store", type=str, default="From config file",
        help=helpmsg, metavar="KEY", dest="apikey")

    # subparser
    subparsers = parser.add_subparsers(dest="cmd", metavar="<COMMAND>", required=True)

    # add subcommands' arguments
    subparsers, _ = arguments.show(subparsers)
    subparsers, _ = arguments.log(subparsers)
    subparsers, _ = arguments.scan(subparsers)
    subparsers, _ = arguments.get(subparsers)
    subparsers, _ = arguments.post(subparsers)

    return parser

def process_args(args):
    """Process command-line arguments.

    Args:
    -----
        args: a argparse.Namespace.

    Returns:
    --------
        An argparse.Namespace with modified content.
    """

    if args.url == "From config file":
        args.url = None

    if args.apikey == "From config file":
        args.apikey = None

    args.config = args.config.expanduser().resolve()

    if args.log_file is not None:
        args.log_file = args.log_file.expanduser().resolve()
        args.log_handler = logging.FileHandler(args.log_file, "w")
        args.log_handler.setFormatter(logging.Formatter(
            "%(asctime)s %(name)s [%(levelname)s] %(message)s",
            "%Y-%m-%d %H:%M:%S"))
    else:
        args.log_handler = logging.NullHandler()

    if args.log_level is None:
        args.log_level = 0
    else:
        args.log_level = getattr(logging, args.log_level.upper())

    return args

def main():
    """Main function of YASync-CLI."""

    parser = get_parser()
    args = parser.parse_args()
    args = process_args(args)

    # get logger and config it
    logger = logging.getLogger("yasynccli")
    logger.setLevel(args.log_level)
    logger.addHandler(args.log_handler)

    # excute command
    logger.debug("Ready to execute command `{}`.".format(args.cmd))
    args.func(args)
    logger.debug("Existing yasync-cli.")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
