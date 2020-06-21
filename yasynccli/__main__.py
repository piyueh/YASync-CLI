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
from . import subcommands

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
    parser_show.set_defaults(func=subcommands.show)

    # add subcommand: scan
    msg = "Scan a directory/file to force synchronization."
    parser_scan = subparsers.add_parser("scan", description=msg, help=msg)
    parser_scan.set_defaults(func=subcommands.scan)
    parser_scan.add_argument("path", action="store", type=str, metavar="PATH", help=msg)

    # add subcommand: get
    msg = "Send a GET request to server. The is for debugging."
    parser_get = subparsers.add_parser("get", description=msg, help=msg)
    parser_get.set_defaults(func=subcommands.get)

    msg = "The GET api endpoint. Options: %(choices)s. "
    parser_get.add_argument(
        "endpoint", action="store", type=str, metavar="ENDPOINT", help=msg,
        choices=subcommands.SyncthingSession._get_apis)

    parser_get.add_argument(
        "args", action="store", type=str, metavar="ARGS", nargs=argparse.REMAINDER,
        help="Parameters of the API endpoint.")

    # add subcommand: post
    msg = "Send a POST request to server. The is for debugging."
    parser_post = subparsers.add_parser("post", description=msg, help=msg)
    parser_post.set_defaults(func=subcommands.post)

    msg = "The POST api endpoint. Options: %(choices)s. "
    parser_post.add_argument(
        "endpoint", action="store", type=str, metavar="ENDPOINT", help=msg,
        choices=subcommands.SyncthingSession._post_apis)

    parser_post.add_argument(
        "args", action="store", type=str, metavar="ARGS", nargs=argparse.REMAINDER,
        help="Parameters of the API endpoint.")

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
