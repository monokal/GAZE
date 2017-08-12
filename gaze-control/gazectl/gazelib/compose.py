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

import subprocess
import sys

from .log import Log
from .template import Template


class Compose(object):
    """ Provides methods to interact with Docker Compose. """

    def __init__(self):
        """
        """

        self.log = Log()
        self.template = Template()

    def up(self, items, action_args=None, template='gaze-compose.yaml.j2',
           project_name='gaze', host='unix://var/run/docker.sock'):
        """
        :param items: Dict: Values required to render the Compose template.
        :param action_args: String: Arguments to the given action.
        :param template: String: Path of the Jinja2 Compose template file.
        :param project_name: String: The Docker project name.
        :param host: String: Path to the Docker socket.
        :return return_code: Int: Return code of the Docker Compose command.
        """

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
            'up', action_args
        ]

        return self._execute(compose_command)

    def down(self, compose_file='gaze-compose.yaml',
             host='unix://var/run/docker.sock'):
        """
        :param compose_file: String: Path of the Docker Compose file.
        :param host: String: Path to the Docker socket.
        :return return_code: Int: Return code of the Docker Compose command.
        """

        compose_command = [
            'docker-compose',
            '-f', '/opt/gazectl/gaze-compose.yaml',
            '-H', host,
            'down'
        ]

        return self._execute(compose_command)

    def _execute(self, compose_command):
        """
        :return return_code: Int: Return code of the Docker Compose command.
        """

        try:
            return_code = subprocess.check_output(compose_command)

        except subprocess.CalledProcessError as e:
            self.log(
                "Failed to execute Docker Compose with exception: \n"
                "{}.".format(e.output), 'exception'
            )
            sys.exit(1)

        return return_code
