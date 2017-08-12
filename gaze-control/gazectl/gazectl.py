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

import argparse
import logging
import sys

import docker
from gazelib.compose import Compose
# Import GAZE modules.
from gazelib.log import Log
from gazelib.template import Template
from tabulate import tabulate
from termcolor import colored

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


class _Gaze(object):
    def __init__(self, args):
        self.args = args
        self.log = Log()

    def __call__(self):
        # Instantiate and call the given class.
        target_class = self.args.func(self.args)
        return target_class()


class _Web(object):
    def __init__(self, args):
        self.log = Log()
        self.template = Template()

    def render_config(self, template='gazeweb-nginx.conf.j2'):
        items = {
            'gazeweb_port': '8080',
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
            destination='/opt/gazectl/gazeweb-nginx.conf'
        )

    def render_index_html(self, template='index.html.j2'):
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


class Bootstrap(object):
    """ Prepare a host for GAZE services deployment. """

    def __init__(self, args):
        """
        :param args: List: Arguments from the command-line.
        """

        self.args = args
        self.log = Log()
        self.web = _Web(self.args)
        self.up = Up(self.args)

        # Instantiate a Docker client.
        try:
            self.docker_client = docker.DockerClient(
                base_url='unix://var/run/docker.sock'
            )

        except docker.errors.APIError:
            self.log("Failed to instantiate the Docker client.", 'exception')
            sys.exit(1)

    def __call__(self):
        """
        """

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
         Turnkey Open Media Centre
         ''', 'blue'))

        self.log("Welcome to GAZE! Let's prepare your system...", 'info')

        # Ensure we can ping to host's Docker daemon.
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

        except:
            self.log(
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
            self.log("    * {}: {}".format(i[0], docker_info[i[1]]), 'success')

        # Render GAZE Web Nginx configuration.
        # self.web.render_config()

        self.log("Bootstrapping complete.", 'info')

        if self.args.noup:
            self.log("To deploy GAZE services, use the \"gaze up\" command.",
                     'info')
        else:
            self.up()


class Up(object):
    def __init__(self, args):
        self.args = args
        self.status = Status(self.args)
        self.log = Log()
        self.compose = Compose()

    def __call__(self):
        items = {
            'gazeweb_port': '8080',
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
    def __init__(self, args):
        self.args = args
        self.log = Log()
        self.compose = Compose()

    def __call__(self):
        self.log("Removing GAZE services...", 'info')
        self.compose.down('/opt/gazectl/gaze-compose.yaml')
        self.log(
            "GAZE services have been removed. Use the \"gaze up\" command to "
            "redeploy.", 'success'
        )


class Status(object):
    def __init__(self, args):
        self.args = args
        self.log = Log()

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
                 "visit GAZE Web at http://localhost/\n", 'info')

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

    #
    # Start "status" subparser.
    parser_status = subparsers.add_parser(
        'status',
        help='list media centre services'
    )

    group_status = parser_status.add_argument_group('required arguments')

    parser_status.set_defaults(func=Status)
    # End "status" subparser.
    #

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
