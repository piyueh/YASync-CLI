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
from . import __version__
from .config import SyncthingConfig

def get_parser():
    """Get an argparse.ArgumentParser with arguments.
    """

    msg = "Use `yasync-cli <COMMAND> -h` to see the help of each sub-command."
    parser = argparse.ArgumentParser(
        "yasync-cli", description="Yet Another Syncthing CLI Tool.\n"+msg,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # version
    parser.add_argument(
        "--version", action='version', version='%(prog)s {}'.format(__version__))

    # logger
    parser.add_argument(
        "--log-level", action="store", default=None, type=str,
        choices=["debug", "info", "warning", "error", "critical"],
        help="log level.", metavar="LEVEL", dest="log_level")

    parser.add_argument(
        "--log-file", action="store", default=None, type=pathlib.Path,
        help="log file path", metavar="FILE", dest="log_file")

    # alternative configuration file, url, and api key
    parser.add_argument(
        "--config", action="store", type=pathlib.Path,
        default=pathlib.Path("~").joinpath(".config", "syncthing", "config.xml"),
        help="alternative configuration file", metavar="CONFIG", dest="config")

    parser.add_argument(
        "--url", action="store", type=str, default="From config file",
        help="alternative URL", metavar="URL", dest="url")

    parser.add_argument(
        "--api-key", action="store", type=str, default="From config file",
        help="alternative API key", metavar="KEY", dest="apikey")

    # subparser
    subparsers = parser.add_subparsers(dest="cmd", metavar="<COMMAND>", required=True)

    # add subcommand: show
    msg = "Show brief information obtained from config file."
    parser_show = subparsers.add_parser("show", description=msg, help=msg)
    parser_show.set_defaults(func=lambda x: print(SyncthingConfig(x.config, x.url, x.apikey)))

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
    """Main function of YASync-CLI.
    """

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
