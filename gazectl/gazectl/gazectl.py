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
import os
import subprocess
import sys

import docker
from termcolor import colored

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

except:
    print("Failed to initialise logging.")
    sys.exit(1)


class Clog(object):
    def __init__(self):
        pass

    def __call__(self, message, level):
        """

        :param message:
        :param level:
        :return: None
        """

        if level == 'info':
            colour = 'blue'

        elif level == 'warning':
            colour = 'yellow'

        elif level == 'debug':
            colour = 'magenta'

        elif level == 'success':
            level = 'info'
            colour = 'green'

        else:
            colour = 'red'

        target_method = getattr(logger, level)
        target_method(colored(message, colour))


class Gaze(object):
    def __init__(self, args):
        self.args = args
        self.clog = Clog()

    def __call__(self):
        # Instantiate and call the given class.
        target_class = self.args.func(self.args)
        return target_class()


class Bootstrap(object):
    def __init__(self, args):
        """

        :param args:
        """

        self.args = args
        self.clog = Clog()
        self.up = Up(self.args)

        # Instantiate a Docker client.
        try:
            self.docker_client = docker.DockerClient(
                base_url='unix://var/run/docker.sock'
            )

        except docker.errors.APIError:
            self.clog("Failed to instantiate the Docker client.", 'exception')
            sys.exit(1)

    def __call__(self):
        """

        :return:
        """

        logger.info(colored(r'''
                                __        .-.
                            .-"` .`'.    /\\|
                    _(\-/)_" ,  .   ,\  /\\\/
                   {(=o^O=)} .   ./,  |/\\\/
                   `-.(Y).-`  ,  |  , |\.-`
                        /~/,_/~~~\,__.-`
                       ////~     //~\\
                     ==`==`    ==`  ==`''', 'magenta'))

        logger.info(colored(r''' ██████╗    █████╗   ███████╗  ███████╗
██╔════╝   ██╔══██╗  ╚══███╔╝  ██╔════╝
██║  ███╗  ███████║    ███╔╝   █████╗  
██║   ██║  ██╔══██║   ███╔╝    ██╔══╝  
╚██████╔╝  ██║  ██║  ███████╗  ███████╗
 ╚═════╝   ╚═╝  ╚═╝  ╚══════╝  ╚══════╝
  Turnkey Open Media Centre
    ''', 'blue'))

        self.clog("Welcome to GAZE! Let's prepare your system...", 'info')
        self.clog("Checking Docker configuration...", 'info')

        # Ensure we can ping to host's Docker daemon.
        self.clog("Checking Docker daemon connectivity...", 'info')

        try:
            self.docker_client.ping()

        except docker.errors.APIError:
            self.clog("Failed to ping the Docker daemon "
                      "(unix://var/run/docker.sock). Are you using the "
                      "\"gaze\" command?", 'exception')

            sys.exit(1)

        self.clog("    * Success!", 'success')

        self.clog("Checking Docker system configuration...", 'info')
        try:
            docker_info = self.docker_client.info()

        except:
            self.clog(
                "Failed to retrieve Docker system info from host.", 'exception'
            )
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
            self.clog("    * {}: {}".format(i[0], docker_info[i[1]]), 'success')

        self.clog("Bootstrapping complete!", 'info')

        if self.args.noup:
            self.clog("To deploy GAZE services, use the \"gaze up\" command.",
                      'info')
        else:
            self.up()


class Compose(object):
    def __init__(self):
        self.clog = Clog()

    def __call__(self, action, action_args=None,
                 compose_file='docker-compose.yaml', project_name='gaze',
                 docker_host='unix://var/run/docker.sock',
                 project_dir=os.path.dirname(os.path.realpath(__file__))):

        compose_command = [
            'docker-compose',
            '-f', compose_file,
            '-p', project_name,
            '-H', docker_host,
            '--project-directory', project_dir,
            action
        ]

        if action_args is not None:
            compose_command.append(action_args)

        try:
            subprocess.check_output(
                compose_command,
                stderr=subprocess.STDOUT
            )

        except subprocess.CalledProcessError as e:
            self.clog(
                "Failed to execute Docker Compose with exception: \n"
                "{}.".format(e.output), 'exception'
            )
            sys.exit(1)


class Up(object):
    def __init__(self, args):
        self.args = args
        self.clog = Clog()
        self.compose = Compose()

    def __call__(self):
        """
        Deploy GAZE containers via Docker Compose.
        """
        self.clog("Deploying GAZE services...", 'info')
        self.compose('up', '-d')
        self.clog("\nThat's it! Your GAZE services can be found here:    "
                  "* http://localhost\n", 'success')


class Down(object):
    def __init__(self, args):
        self.args = args
        self.clog = Clog()
        self.compose = Compose()

    def __call__(self):
        self.clog("Removing GAZE services...", 'info')
        self.compose('down')
        self.clog("    * Done!", 'success')


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

    #
    # Start "up" subparser.
    parser_up = subparsers.add_parser(
        'up',
        help='deploy media centre services'
    )

    group_up = parser_up.add_argument_group('required arguments')

    parser_up.set_defaults(func=Up)
    # End "up" subparser.
    #

    #
    # Start "down" subparser.
    parser_down = subparsers.add_parser(
        'down',
        help='remove media centre services'
    )

    group_down = parser_down.add_argument_group('required arguments')

    parser_down.set_defaults(func=Down)
    # End "down" subparser.
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
