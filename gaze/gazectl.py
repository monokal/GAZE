#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
               GAZE
     Turnkey Open Media Center
                 __        .-.
             .-"` .`'.    /\\|
     _(\-/)_" ,  .   ,\  /\\\/     =o O=
    {(=o^O=)} .   ./,  |/\\\/
    `-.(Y).-`  ,  |  , |\.-`
         /~/,_/~~~\,__.-`   =O o=
        ////~    // ~\\
      ==`==`   ==`   ==`
        gaze.monokal.io
"""

import argparse
import logging
import os
import sys

from gazelib.core.bootstrap import GazeBootstrap
from gazelib.core.config import GazeConfig
from gazelib.core.helpers import GazeHelper
from gazelib.core.log import GazeLog

# Initialise a global logger.
try:
    logger = logging.getLogger('gaze')
    logger.setLevel(logging.INFO)

    # We're in Docker, so just log to stdout.
    out = logging.StreamHandler(sys.stdout)
    out.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(message)s")
    out.setFormatter(formatter)
    logger.addHandler(out)

except Exception as e:
    print("Failed to initialise logging with exception:\n{}".format(e))
    sys.exit(1)


class _Gaze(object):
    def __init__(self, args):
        self.args = args
        self.log = GazeLog()
        self.helpers = GazeHelper()
        self.config = GazeConfig()

    def __call__(self):
        print(self.helpers.ascii_banner())
        config = self.config.load(self.args.config)

        # Instantiate and call the given class.
        target_class = self.args.func(self.args, config)
        return target_class()


def main():
    """
    Handle argument routing.
    :return: None
    """

    # Configure argument parsing.
    parser = argparse.ArgumentParser(
        prog="gaze",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Top-level arguments.
    parser.add_argument(
        "-d",
        "--debug",
        required=False,
        action="store_true",
        help="output in debug verbosity"
    )

    parser.add_argument(
        "-c",
        "--config",
        required=False,
        type=str,
        nargs=1,
        metavar='CONFIG_PATH',
        help="path to the gaze.yaml file",
        default="{}/gaze.yaml".format(
            os.path.dirname(os.path.realpath(__file__)))
    )

    # Subparser arguments.
    subparsers = parser.add_subparsers()

    #
    # Start "bootstrap" subparser.
    parser_bootstrap = subparsers.add_parser(
        'bootstrap',
        help='bootstrap a GAZE host'
    )

    parser_bootstrap.set_defaults(func=GazeBootstrap)
    # End "bootstrap" subparser.
    #

    #
    # Start "jackett" subparser.
    # parser_jackett = subparsers.add_parser(
    #     'jackett',
    #     help='manage the Jackett service'
    # )
    #
    # group_jackett = parser_jackett.add_argument_group('required arguments')
    #
    # group_jackett.add_argument('--up',
    #                         action="store_true",
    #                         help="deploy a Jackett service")
    #
    # group_jackett.add_argument('--down',
    #                         action="store_true",
    #                         help="stop the Jackett service")
    #
    # group_jackett.add_argument('--destroy',
    #                         action="store_true",
    #                         help="destroy the Jackett service")
    #
    # parser_jackett.set_defaults(func=GazeJackett)
    # End "jackett" subparser.
    #

    try:
        args = parser.parse_args()

    except Exception as e:
        print("Failed to parse arguments with exception:\n{}".format(e))
        sys.exit(1)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    # Log usage to analytics.
    # analytics.track_event('GAZE Command', args.func)

    client = _Gaze(args)

    try:
        return client()

    except AttributeError as e:
        print("Failed to parse arguments with exception:\n{}\n".format(e))
        parser.print_help()


if __name__ == "__main__":
    main()
