#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
               GAZE
     Turnkey Open Media Centre
                 __        .-.
             .-"` .`'.    /\\|
     _(\-/)_" ,  .   ,\  /\\\/     =o O=
    {(=o^O=)} .   ./,  |/\\\/
    `-.(Y).-`  ,  |  , |\.-`
         /~/,_/~~~\,__.-`   =O o=
        ////~    // ~\\
      ==`==`   ==`   ==`
             monokal.io
"""

__author__ = "Daniel Middleton"
__email__ = "d@monokal.io"

import argparse
import logging
import sys

# Initialise a global logger.
try:
    logger = logging.getLogger('GAZE')
    logger.setLevel(logging.INFO)

    # We're in Docker, so just log to stdout.
    out = logging.StreamHandler(sys.stdout)
    out.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
        "%d-%m-%Y %H:%M:%S"
    )
    out.setFormatter(formatter)
    logger.addHandler(out)

except:
    print("Failed to initialise logging.")
    sys.exit(1)


class Gaze(object):
    def __init__(self, args):
        """ Initialise GAZE. Load config, etc.

        :param args: A Dict of arguments from the command-line.
        """

        self.config = self.load_config(args.config)
        logger.debug("Loaded config: {}".format(self.config))

    def __call__(self, args):
        """ Orchestrate GAZE execution.

        :param args: A Dict of arguments from the command-line.
        :return:
        """

        # TODO


class Init(object):
    def __init__(self):
        # TODO

    def __call__(self):
        print("""
               GAZE
     Turnkey Open Media Centre
                 __        .-.
             .-"` .`'.    /\\|
     _(\-/)_" ,  .   ,\  /\\\/     =o O=
    {(=o^O=)} .   ./,  |/\\\/
    `-.(Y).-`  ,  |  , |\.-`
         /~/,_/~~~\,__.-`   =O o=
        ////~    // ~\\
      ==`==`   ==`   ==`
             monokal.io\n""")

        logger.info("Bootstrapping GAZE...")


def main():
    # Configure argument parsing.
    parser = argparse.ArgumentParser(
        prog="GAZE",
        description="Turnkey Open Media Centre."
    )

    #
    # Top-level arguments.
    #
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
        default=['./config.yaml'],
        required=False,
        type=str,
        nargs=1,
        metavar='PATH',
        help="path of the GAZE config file"
    )

    subparsers = parser.add_subparsers()

    #
    # "init" parser.
    #
    parser_init = subparsers.add_parser(
        'init',
        help='bootstrap a GAZE host'
    )

    parser_init.set_defaults(func=Init)

    #
    # "up" parser.
    #
    parser_up = subparsers.add_parser(
        'up',
        help='deploy GAZE services'
    )

    group_up.add_argument(
        '--ask',
        required=False,
        action="store_true",
        help="cherry-pick services to install"
    )

    parser_init.set_defaults(func=Init)

    try:
        args = parser.parse_args()

    except Exception:
        logger.exception("Failed to parse arguments.")
        sys.exit(1)

    # Turn on debug output if -d/--debug was passed.
    if args.debug:
        logger.setLevel(logging.DEBUG)

    client = Gaze(args)
    client(args)


if __name__ == "__main__":
    main()
