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

from termcolor import colored, cprint
import docker

# Initialise a global logger.
try:
    logger = logging.getLogger('gaze')
    logger.setLevel(logging.INFO)

    # We're in Docker, so just log to stdout.
    out = logging.StreamHandler(sys.stdout)
    out.setLevel(logging.DEBUG)
    formatter = logging.Formatter(" %(message)s")
    out.setFormatter(formatter)
    logger.addHandler(out)

except:
    print("Failed to initialise logging.")
    sys.exit(1)


class Gaze(object):
    def __init__(self, args):
        self.args = args

    def __call__(self):
        # Instantiate and call the given class.
        target_class = self.args.func(self.args)
        return target_class()


class Bootstrap(object):
    def __init__(self, args):
        self.args = args

        # Instantiate a Docker client.
        try:
            self.docker_client = docker.DockerClient(
                base_url='unix://var/run/docker.sock'
            )

        except docker.errors.APIError:
            logger.exception(
                colored("Failed to instantiate the Docker client.", 'red'))
            sys.exit(1)

        # Ensure we can ping to host's Docker daemon.
        try:
            self.docker_client.ping()

        except docker.errors.APIError:
            logger.exception(colored(
                "Failed to ping the Docker daemon (unix://var/run/docker.sock)."
                "Are you using the \"gaze\" command?", 'red'))

            sys.exit(1)

    def __call__(self):
        logger.info(colored(r'''
                                 __        .-.
                             .-"` .`'.    /\\|
                     _(\-/)_" ,  .   ,\  /\\\/
                    {(=o^O=)} .   ./,  |/\\\/
                    `-.(Y).-`  ,  |  , |\.-`
                         /~/,_/~~~\,__.-`
                        ////~    // ~\\
                      ==`==`   ==`   ==`
  ██████╗    █████╗   ███████╗  ███████╗
 ██╔════╝   ██╔══██╗  ╚══███╔╝  ██╔════╝
 ██║  ███╗  ███████║    ███╔╝   █████╗  
 ██║   ██║  ██╔══██║   ███╔╝    ██╔══╝  
 ╚██████╔╝  ██║  ██║  ███████╗  ███████╗
  ╚═════╝   ╚═╝  ╚═╝  ╚══════╝  ╚══════╝
   Turnkey Open Media Centre
    ''', 'blue'))

        logger.info(
            colored("Welcome to GAZE! Let's prepare your system...", 'blue'))

        logger.info(colored("Checking Docker configuration...", 'blue'))
        try:
            docker_info = self.docker_client.info()

        except:
            logger.exception(
                colored("Failed to retrieve Docker system info from host.",
                        'red'))
            sys.exit(1)

        info_items = [
            ['System time', 'SystemTime'],
            ['Server version', 'ServerVersion'],
            ['Operating System', 'OperatingSystem'],
            ['Architecture', 'Architecture'],
            ['Kernel version', 'KernelVersion'],
            ['CPUs', 'NCPU'],
            ['Memory', 'MemTotal'],
            ['Driver', 'Driver'],
            ['Runtime', 'DefaultRuntime'],
            ['Debug', 'Debug']
        ]

        for i in info_items:
            logger.info(
                colored("    * {}: {}", 'blue').format(i[0], docker_info[i[1]]))


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
        logger.exception(colored("Failed to parse arguments.", 'red'))
        sys.exit(1)

    # Turn on debug output if -d/--debug was passed.
    if args.debug:
        logger.setLevel(logging.DEBUG)

    client = Gaze(args)
    return client()


if __name__ == "__main__":
    main()
