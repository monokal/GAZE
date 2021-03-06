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

from gazelib.core.error import *
from gazelib.core.log import GazeLog


class GazeVolume(object):
    """ Provides methods to manage Docker Volumes. """

    def __init__(self):
        self.log = GazeLog()

        # Instantiate a Docker client.
        try:
            self.docker_client = docker.DockerClient(
                base_url='unix://var/run/docker.sock'
            )

        except docker.errors.APIError:
            self.log("Failed to instantiate the Docker client.", 'exception')
            sys.exit(1)

    def list(self):
        """
        Return all Docker Volumes.

        :return volumes: List: Docker Volume objects.
        """

        try:
            volumes = self.docker_client.volumes.list()

        except docker.errors.APIError:
            self.log("Failed to get Docker Volumes.", 'exception')
            sys.exit(1)

        return volumes

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

        except docker.errors.NotFound:
            raise GazeVolumeNotFound

        except docker.errors.APIError:
            self.log(
                "Failed to get Docker Volume ({}).".format(volume_id),
                'info'
            )
            sys.exit(1)

        return volume

    def create(self, name, driver='local', driver_opts=None):
        """
        Create a Docker Volume.

        :param name: (str) Name of the Docker Volume.
        :param driver: (str) Name of the Volume driver.
        :param driver_opts:
        :return:
        """

        try:
            volume = self.get(name)
            self.log(
                "The Docker Volume ({}) already exists.".format(name), 'info'
            )

        except GazeVolumeNotFound:
            self.log("Creating Docker Volume ({})...".format(name), 'info')
            try:
                volume = self.docker_client.volumes.create(
                    name=name,
                    driver=driver,
                    driver_opts=driver_opts,
                    labels={
                        "gaze.volume": name
                    }
                )

                self.log("OK!", 'success')

            except docker.errors.APIError:
                self.log(
                    "Failed to create Docker Volume ({}).".format(name),
                    'exception'
                )
                sys.exit(1)

        # self.log("Got Docker Volume:\n{}".format(volume.attrs['Mountpoint']), 'debug')
        self.log("Got Docker Volume:\n{}".format(volume.attrs), 'debug')
        return volume
