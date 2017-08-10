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

import os


class Compose(object):
    def __init__(self):
        pass

    def __call__(self,
                 action,
                 items,
                 action_args=None,
                 template='gaze-compose.yaml.j2',
                 project_name='gaze',
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