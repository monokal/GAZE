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

from gazelib.core.helpers import GazeHelper
from gazelib.core.log import GazeLog
from gazelib.docker.container import GazeContainer


class GazeJackett(object):
    """ Manage the Jackett service. """

    def __init__(self, args, config):
        """
        :param args: (list) Arguments from the command-line.
        :param config: (dict) Config loaded from the YAML file.
        """

        self.args = args
        self.config = config

        self.helpers = GazeHelper()
        self.log = GazeLog()
        self.container = GazeContainer()

    def create(self):
        # TODO: Create service volume.

        self.container.run(
            name='gaze_jackett',
            image='linuxserver/jackett:latest',
            environment=None,
            volumes=None,
            network_mode=None,
            networks=None,
            ports=None,
            labels=["gaze.service=radarr"],
            cap_add=None,
            restart_policy=None,
            command=None
        )

    def remove(self):
        self.container.remove()

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        self.stop()
        self.start()
