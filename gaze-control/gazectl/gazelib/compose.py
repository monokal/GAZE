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

import os
import subprocess
import sys

from .log import Log
from .template import Template


class Compose(object):
    """ Provides methods to interact with Docker Compose. """

    def __init__(self, debug=False):
        """
        :param debug: Boolean: Set the logger to debug verbosity.
        """

        self.log = Log(debug)
        self.template = Template(debug)

    def __call__(self,
                 action,
                 items,
                 action_args=None,
                 template='gaze-compose.yaml.j2',
                 project_name='gaze',
                 host='unix://var/run/docker.sock',
                 project_dir=os.path.dirname(os.path.realpath(__file__))):
        """
        :param action: String: The top-level Docker Compose command to execute.
        :param items: Dict: Values required to render the Compose template.
        :param action_args: String: Arguments to the given action.
        :param template: String: Path of the Jinja2 Compose template file.
        :param project_name: String: The Docker project name.
        :param host: String: Path to the Docker socket.
        :param project_dir: String: Path to the Docker project.
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
            '--project-directory', project_dir,
            action
        ]

        if action_args is not None:
            compose_command.append(action_args)

        try:
            return_code = subprocess.check_output(compose_command)

        except subprocess.CalledProcessError as e:
            self.log(
                "Failed to execute Docker Compose with exception: \n"
                "{}.".format(e.output), 'exception'
            )
            sys.exit(1)

        return return_code
