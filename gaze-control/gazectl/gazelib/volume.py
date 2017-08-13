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

import sys

import docker

from .error import *
from .log import GazeLog


class GazeVolume(object):
    """ Provides methods to manage Docker Volumes. """

    def __init__(self):
        """
        """

        self.log = GazeLog()

        # Instantiate a Docker client.
        try:
            self.docker_client = docker.DockerClient(
                base_url='unix://var/run/docker.sock'
            )

        except docker.errors.APIError:
            self.log("Failed to instantiate the Docker client.", 'exception')
            sys.exit(1)

    def get(self, volume_id):
        """
        Get information about a Docker Volume.

        :param volume_id: String: ID of the Docker Volume.
        :return volume: Docker Volume object.
        """

        try:
            volume = self.docker_client.volumes.get(
                volume_id=volume_id
            )

        except docker.errors.APIError:
            self.log(
                "Failed to get Docker Volume ({}).".format(volume_id),
                'exception'
            )
            sys.exit(1)

        except docker.errors.NotFound:
            self.log(
                "The Docker Volume ({}) does not exist.".format(volume_id),
                'info'
            )
            raise GazeVolumeNotFound

        return volume

    def create(self, name, driver, labels, driver_opts=None):
        """
        Create a Docker Volume.

        :param name:
        :param driver:
        :param driver_opts:
        :param labels:
        :return:
        """

        try:
            volume = self.docker_client.volumes.create(
                name=name,
                driver=driver,
                driver_opts=driver_opts,
                labels=labels
            )
        except docker.errors.APIError:
            self.log(
                "Failed to create Docker Volume ({}).".format(name), 'exception'
            )
            sys.exit(1)

        return volume
