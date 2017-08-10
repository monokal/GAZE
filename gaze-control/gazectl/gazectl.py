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
import os
import subprocess
import sys

import docker
from jinja2 import Environment, FileSystemLoader
from tabulate import tabulate
from termcolor import colored

# GAZE modules.
from .gazelib.compose import Compose
from .gazelib.template import Template
from .gazelib.volume import Volume

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

except:
    print("Failed to initialise logging.")
    sys.exit(1)


#
# Internal classes.
#
class _Clog(object):
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


class _Gaze(object):
    def __init__(self, args):
        self.args = args
        self.clog = _Clog()

    def __call__(self):
        # Instantiate and call the given class.
        target_class = self.args.func(self.args)
        return target_class()


class _Compose(object):
    def __init__(self):
        self.clog = _Clog()
        self.template = _Template()

    def __call__(self, action, items, action_args=None,
                 template='gaze-compose.yaml.j2', project_name='gaze',
                 host='unix://var/run/docker.sock',
                 project_dir=os.path.dirname(os.path.realpath(__file__))):

        # Render the GAZE Docker Compose file.
        self.template.render(
            template=template,
            items=items,
            destination='/opt/gazectl/gaze-compose.yaml'
        )

        compose_command = [
            'docker-compose',
            '-f', '/opt/gazectl/gaze-compose.yaml',
            '-p', project_name,
            '-H', host,
            '--project-directory', project_dir,
            action
        ]

        if action_args is not None:
            compose_command.append(action_args)

        try:
            subprocess.check_output(compose_command)

        except subprocess.CalledProcessError as e:
            self.clog(
                "Failed to execute Docker Compose with exception: \n"
                "{}.".format(e.output), 'exception'
            )
            sys.exit(1)


class _GazeWeb(object):
    def __init__(self):
        self.clog = _Clog()
        self.template = _Template()

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
            destination='/etc/nginx/conf.d/gazeweb.conf'
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


class _Template(object):
    def __init__(self):
        self.clog = _Clog()

    def render(self, template, items, destination):
        """
        Render a Jinja2 template to file.
        :param template:
        :param items:
        :param destination:
        :return:
        """
        self.clog("Rendering template ({})...".format(destination), 'info')

        j2_env = Environment(loader=FileSystemLoader("templates"))
        rendered = j2_env.get_template(template).render(items)

        with open(destination, "w") as file:
            file.write(rendered)

        self.clog("Rendered template ({}):\n{}".format(destination, rendered),
                  'debug')


#
# User-called classes.
#
class Bootstrap(object):
    def __init__(self, args):
        """

        :param args:
        """

        self.args = args
        self.clog = _Clog()
        self.gazeweb = _GazeWeb()
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

        self.clog("Welcome to GAZE! Let's prepare your system...", 'info')

        # Ensure we can ping to host's Docker daemon.
        self.clog("Checking Docker daemon connectivity...", 'info')

        try:
            self.docker_client.ping()

        except docker.errors.APIError:
            self.clog(
                "Failed to ping the Docker daemon (unix://var/run/docker.sock)."
                " Are you using the \"gaze\" command?", 'exception'
            )
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

        self.clog("Rendering GAZE Web configuration...", 'info')
        self.gazeweb.render_config()
        self.clog("    * Success!", 'success')

        self.clog("Bootstrapping complete.", 'info')

        if self.args.noup:
            self.clog("To deploy GAZE services, use the \"gaze up\" command.",
                      'info')
        else:
            self.up()


class _Volume(object):
    def __init__(self):
        self.clog = _Clog()

        # Instantiate a Docker client.
        try:
            self.docker_client = docker.DockerClient(
                base_url='unix://var/run/docker.sock'
            )

        except docker.errors.APIError:
            self.clog("Failed to instantiate the Docker client.", 'exception')
            sys.exit(1)

    def get(self, volume_id):
        try:
            volume = self.docker_client.volumes.get(
                volume_id=volume_id
            )
        except docker.errors.APIError:
            self.clog(
                "Failed to get Docker Volume ({}).".format(volume_id),
                'exception'
            )
            sys.exit(1)

    def create(self, name, driver, driver_opts, labels):
        try:
            volume = self.docker_client.volumes.create(
                name=name,
                driver=driver,
                driver_opts=driver_opts,
                labels=labels
            )
        except docker.errors.APIError:
            self.clog(
                "Failed to create Docker Volume ({}).".format(name), 'exception'
            )
            sys.exit(1)


class Up(object):
    def __init__(self, args):
        self.args = args
        self.status = Status(self.args)
        self.clog = _Clog()
        self.compose = _Compose()

    def __call__(self):
        items = {
            'gazeweb_port': '8080',
            'plex_claim': 'test',
            'plex_ip': '0.0.0.0',
            'uid': '1000',
            'gid': '1000'
        }

        self.clog("Deploying GAZE services...", 'info')
        self.compose('up', items, '-d')
        self.clog("That's it!", 'success')
        self.status()


class Down(object):
    def __init__(self, args):
        self.args = args
        self.clog = _Clog()
        self.compose = _Compose()

    def __call__(self):
        self.clog("Removing GAZE services...", 'info')
        self.compose('down')
        self.clog(
            "GAZE services have been removed. Use the \"gaze up\" command to "
            "redeploy.", 'success'
        )


class Status(object):
    def __init__(self, args):
        self.args = args
        self.clog = _Clog()

        # Instantiate a Docker client.
        try:
            self.docker_client = docker.DockerClient(
                base_url='unix://var/run/docker.sock'
            )

        except docker.errors.APIError:
            self.clog("Failed to instantiate the Docker client.", 'exception')
            sys.exit(1)

    def __call__(self):
        self.clog("Your GAZE services are listed below. To access them, "
                  "visit GAZE Web at http://localhost/\n", 'info')

        try:
            containers = self.docker_client.containers.list(
                all=True,
                filters={'label': 'gaze.service'}
            )

        except docker.errors.APIError:
            self.clog(
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
        logger.exception(colored("Failed to parse arguments.", 'red'))
        sys.exit(1)

    # Turn on debug output if -d/--debug was passed.
    if args.debug:
        logger.setLevel(logging.DEBUG)

    client = _Gaze(args)
    return client()


if __name__ == "__main__":
    main()
