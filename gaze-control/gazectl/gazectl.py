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
import sys

import docker
from tabulate import tabulate
from termcolor import colored

from gazelib.compose import GazeCompose
from gazelib.config import GazeConfig
from gazelib.container import GazeContainer
from gazelib.log import GazeLog
from gazelib.network import GazeNetwork
from gazelib.template import GazeTemplate
from gazelib.volume import GazeVolume

# Initialise a global logger.
try:
    logger = logging.getLogger('gaze')
    logger.setLevel(logging.INFO)

    # We're in Docker, so just log to stdout.
    out = logging.StreamHandler(sys.stdout)
    out.setLevel(logging.DEBUG)
    formatter = logging.Formatter("{} %(message)s".format(
        colored('[GAZE]', 'magenta'))
    )
    out.setFormatter(formatter)
    logger.addHandler(out)

except Exception as e:
    print("Failed to initialise logging with exception:\n{}".format(e))
    sys.exit(1)


#
# User called Classes.
#

class Bootstrap(object):
    """ Prepare a host for GAZE services deployment. """

    def __init__(self, args, config):
        """
        :param args: (list) Arguments from the command-line.
        """

        self.args = args
        self.config = config

        self.log = GazeLog()
        self.volume = GazeVolume()
        self.network = GazeNetwork()
        self.container = GazeContainer()

        self.proxy = _Proxy(self.args)
        self.up = Up(self.args, self.config)

        # Instantiate a Docker client.
        try:
            self.docker_client = docker.DockerClient(
                base_url='unix://var/run/docker.sock'
            )

        except docker.errors.APIError:
            self.log("Failed to instantiate the Docker client.", 'exception')
            sys.exit(1)

    def __call__(self):
        print(colored(r'''
                                       __        .-.
                                   .-"` .`'.    /\\|
                           _(\-/)_" ,  .   ,\  /\\\/
                          {(=o^O=)} .   ./,  |/\\\/
                          `-.(Y).-`  ,  |  , |\.-`
                               /~/,_/~~~\,__.-`
                              ////~     //~\\
                            ==`==`    ==`  ==`''', 'magenta'))
        print(colored(r'''        ██████╗    █████╗   ███████╗  ███████╗
       ██╔════╝   ██╔══██╗  ╚══███╔╝  ██╔════╝
       ██║  ███╗  ███████║    ███╔╝   █████╗  
       ██║   ██║  ██╔══██║   ███╔╝    ██╔══╝  
       ╚██████╔╝  ██║  ██║  ███████╗  ███████╗
        ╚═════╝   ╚═╝  ╚═╝  ╚══════╝  ╚══════╝
         Turnkey Open Media Center
         ''', 'blue'))

        self.log("Welcome to GAZE! Let's prepare your system...", 'info')

        # Ensure we can ping the host's Docker daemon.
        self.log("Checking Docker daemon connectivity...", 'info')
        try:
            self.docker_client.ping()

        except docker.errors.APIError:
            self.log(
                "Failed to ping the Docker daemon (unix://var/run/docker.sock)."
                " Are you using the \"gaze\" command?", 'exception'
            )
            sys.exit(1)

        self.log("    * Success!", 'success')

        self.log("Checking Docker system configuration...", 'info')
        try:
            docker_info = self.docker_client.info()

        except Exception as e:
            self.log(
                "Failed to retrieve Docker system info from host with "
                "exception:\n{}".format(e), 'exception'
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
            self.log("    * {}: {}".format(i[0], docker_info[i[1]]), 'success')

        # Bootstrap the "gaze-share" Docker Volume.
        volume = self.volume.create(name='gaze-share')

        # Bootstrap the "gaze-internal" Docker Network.
        # network = self.network.create(name='gaze-internal')

        # Render GAZE Proxy Nginx configuration.
        self.proxy.render_config(
            destination="{}/gazeproxy-nginx.conf".format(
                volume.attrs['Mountpoint']
            )
        )

        self.log("Bootstrapping complete.", 'info')

        if self.args.noup:
            self.log("To deploy GAZE services, use the \"gaze up\" command.",
                     'info')
        else:
            self.up()


class Up(object):
    def __init__(self, args, config):
        self.args = args
        self.config = config
        self.status = Status(self.args, self.config)
        self.log = GazeLog()
        self.compose = GazeCompose()

    def __call__(self):
        items = {
            'gazeproxy_port': '8080',
            'plex_claim': 'test',
            'plex_ip': '0.0.0.0',
            'uid': '1000',
            'gid': '1000'
        }

        self.log("Deploying GAZE services...", 'info')
        self.compose.up(items, '-d')
        self.log("That's it!", 'success')
        self.status()


class Down(object):
    def __init__(self, args, config):
        self.args = args
        self.config = config
        self.log = GazeLog()
        self.compose = GazeCompose()

    def __call__(self):
        self.log("Removing GAZE services...", 'info')
        self.compose.down('/opt/gazectl/gaze-compose.yaml')
        self.log(
            "GAZE services have been removed. Use the \"gaze up\" command to "
            "redeploy.", 'success'
        )


# class Volume(object):
#     def __init__(self, args):
#         self.args = args
#         self.log = GazeLog()
#         self.volume = GazeVolume()
#
#     def __call__(self):
#         pass


class Status(object):
    def __init__(self, args, config):
        self.args = args
        self.config = config
        self.log = GazeLog()

        # Instantiate a Docker client.
        try:
            self.docker_client = docker.DockerClient(
                base_url='unix://var/run/docker.sock'
            )

        except docker.errors.APIError:
            self.log("Failed to instantiate the Docker client.", 'exception')
            sys.exit(1)

    def __call__(self):
        self.log("Your GAZE services are listed below. To access them, "
                 "visit GAZE Proxy at http://localhost/\n", 'info')

        try:
            containers = self.docker_client.containers.list(
                all=True,
                filters={'label': 'gaze.service'}
            )

        except docker.errors.APIError:
            self.log(
                "Failed to retrieve Docker container info from host.",
                'exception'
            )
            sys.exit(1)

        table_headers = ['Service', 'Container', 'Status']
        table_data = []

        for i in containers:
            table_data.append(
                [
                    str(i.labels['gaze.service']).upper(),
                    i.name,
                    str(i.status).upper()
                ]
            )

        print(
            tabulate(
                tabular_data=table_data,
                headers=table_headers,
                tablefmt='simple'
            ), "\n"
        )


#
# Internally called Classes.
#

class _Gaze(object):
    def __init__(self, args):
        self.args = args
        self.log = GazeLog()
        self.config = GazeConfig()

    def __call__(self):
        # Instantiate and call the given class.
        target_class = self.args.func(self.args, self.config)
        return target_class()


class _Proxy(object):
    def __init__(self, args):
        self.log = GazeLog()
        self.template = GazeTemplate()

    def render_config(self, destination, template='gazeproxy-nginx.conf.j2'):
        items = {
            'gazeproxy_port': '8080',
            'services': {
                'plex': '32400',
                'plexpy': '8181',
                'transmission': '9091',
                'sonarr': '8989',
                'radarr': '7878',
                'jackett': '9117',
                'ombi': '3579'
            }
        }

        self.template.render(
            template=template,
            items=items,
            destination=destination
        )

    def render_index(self, template='index.html.j2'):
        items = {
            'services': {
                'plex': '32400',
                'plexpy': '8181',
                'transmission': '9091',
                'sonarr': '8989',
                'radarr': '7878',
                'jackett': '9117',
                'ombi': '3579'
            }
        }

        self.template.render(
            template=template,
            items=items,
            destination='/some/path/index.html'
        )


def main():
    # Configure argument parsing.
    parser = argparse.ArgumentParser(
        prog="gaze",
        description="Turnkey Open Media Center."
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
        help='deploy media center services'
    )

    parser_up.set_defaults(func=Up)
    # End "up" subparser.
    #

    #
    # Start "down" subparser.
    parser_down = subparsers.add_parser(
        'down',
        help='remove media center services'
    )

    group_down = parser_down.add_argument_group('required arguments')

    parser_down.set_defaults(func=Down)
    # End "down" subparser.
    #

    #
    # Start "status" subparser.
    parser_status = subparsers.add_parser(
        'status',
        help='list media center services'
    )

    parser_status.set_defaults(func=Status)
    # End "status" subparser.
    #

    # #
    # # Start "volume" subparser.
    # parser_volume = subparsers.add_parser(
    #     'volume',
    #     help='manage GAZE volumes'
    # )
    #
    # group_volume = parser_volume.add_argument_group('required arguments')
    #
    # group_volume.add_argument('--create',
    #                            nargs=1,
    #                            metavar='NAME',
    #                            help="create a GAZE volume")
    #
    # parser_volume.set_defaults(func=Volume)
    # # End "volume" subparser.
    # #

    try:
        args = parser.parse_args()

    except Exception:
        print("Failed to parse arguments.")
        sys.exit(1)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    client = _Gaze(args)
    return client()


if __name__ == "__main__":
    main()
