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

import docker

# Initialise a global logger.
try:
    logger = logging.getLogger('gaze')
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
        self.args = args

    def __call__(self):
        # Instanciate and call the given class.
        target_class = self.args.func(self.args)
        return target_class()


class Bootstrap(object):
    def __init__(self, args):
        try:
            self.docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
            self.docker_info = self.docker_client.info()

        except Exception as e:
            logger.exception("Failed to connect to the Docker daemon (unix://var/run/docker.sock). Are you using the \"gaze\" command?)
            sys.exit(1)

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

        logger.info("Welcome to GAZE! Let's check a few things...")

        logger.info("Checking Docker host:")
        logger.info("  * System time: {}".format(self.docker_info['SystemTime']))
        logger.info("  * Server version: {}".format(self.docker_info['ServerVersion']))
        logger.info("  * Operating System: {}".format(self.docker_info['OperatingSystem']))
        logger.info("  * Architecture: {}".format(self.docker_info['Architecture']))
        logger.info("  * Kernel version: {}".format(self.docker_info['KernelVersion']))
        logger.info("  * CPUs: {}".format(self.docker_info['NCPU']))
        logger.info("  * Memory: {}".format(self.docker_info['MemTotal']))
        logger.info("  * Driver: {}".format(self.docker_info['Driver']))
        logger.info("  * Default Runtime: {}".format(self.docker_info['DefaultRuntime']))
        logger.info("  * Debug: {}".format(self.docker_info['Debug']))


def main():
    # Configure argument parsing.
    parser = argparse.ArgumentParser(
        prog="gaze",
        description="Turnkey Open Media Centre."
    )

    # Top-level arguments.
    parser.add_argument(
        "-d",
        "--debug",
        required=False,
        action="store_true",
        help="output in debug verbosity"
    )

    # Subparser arguments.
    subparsers = parser.add_subparsers()

    #
    # Start "bootstrap" subparser.
    parser_bootstrap = subparsers.add_parser(
        'bootstrap',
        help='bootstrap a GAZE host'
    )

    group_bootstrap = parser_bootstrap.add_argument_group('required arguments')

    group_bootstrap.add_argument(
        '--noup',
        required=False,
        action="store_true",
        help="don't run \"gaze up\" after bootstrapping"
    )

    parser_bootstrap.set_defaults(func=Bootstrap)
    # End "bootstrap" subparser.
    #

    try:
        args = parser.parse_args()

    except Exception:
        logger.exception("Failed to parse arguments.")
        sys.exit(1)

    # Turn on debug output if -d/--debug was passed.
    if args.debug:
        logger.setLevel(logging.DEBUG)

    client = Gaze(args)
    return client()


if __name__ == "__main__":
    main()
