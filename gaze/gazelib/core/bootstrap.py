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

import sys

import docker
from gazelib.core.helpers import GazeHelper
from gazelib.core.log import GazeLog
from gazelib.docker.container import GazeContainer
from gazelib.docker.network import GazeNetwork
from gazelib.docker.volume import GazeVolume


class GazeBootstrap(object):
    """ Prepare a host for GAZE services. """

    def __init__(self, args, config, docker_url='unix://var/run/docker.sock'):
        """
        :param args: (list) Arguments from the command-line.
        :param config: (dict) Config loaded from the YAML file.
        """

        self.args = args
        self.config = config
        self.docker_url = docker_url

        self.helpers = GazeHelper()
        self.log = GazeLog()
        self.volume = GazeVolume()
        self.network = GazeNetwork()
        self.container = GazeContainer()

        # Instantiate a Docker client.
        try:
            self.docker_client = docker.DockerClient(
                base_url=self.docker_url
            )

        except docker.errors.APIError:
            self.log("Failed to instantiate the Docker client.", 'exception')
            sys.exit(1)

    def __call__(self):
        self.log("Let's prepare your system...", 'info')

        # Ensure we can ping the host's Docker daemon.
        self.log("Checking Docker daemon connectivity...", 'info')
        try:
            self.docker_client.ping()

        except docker.errors.APIError:
            self.log(
                "Failed to ping the Docker daemon ({})."
                " Are you using the \"gaze\" command?".format(self.docker_url),
                'exception'
            )
            sys.exit(1)

        self.log("OK!", 'success')

        self.log("Checking Docker system configuration...", 'info')
        try:
            docker_info = self.docker_client.info()

        except Exception as e:
            self.log(
                "Failed to retrieve Docker system info from host with "
                "exception:\n{}".format(e), 'exception'
            )
            sys.exit(1)

        info_items = (
            ('System time', 'SystemTime'),
            ('Server version', 'ServerVersion'),
            ('Operating System', 'OperatingSystem'),
            ('Architecture', 'Architecture'),
            ('Kernel version', 'KernelVersion'),
            ('CPUs', 'NCPU'),
            ('Memory', 'MemTotal'),
            ('Driver', 'Driver'),
            ('Runtime', 'DefaultRuntime'),
            ('Debug', 'Debug'),
        )

        for i in info_items:
            self.log("{}: {}".format(i[0], docker_info[i[1]]), 'success')

        # Bootstrap the "gaze-share" Docker Volume.
        self.volume.create(name='gaze_share')

        # Bootstrap the "gaze-internal" Docker Network.
        self.network.create(name='gaze_internal')

        self.log("Bootstrapping complete.", 'info')
