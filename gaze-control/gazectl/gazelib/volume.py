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

from .log import Log


class Volume(object):
    """ Provides methods to manage Docker Volumes. """

    def __init__(self, debug=False):
        """
        :param debug: Boolean: Set the logger to debug verbosity.
        """

        self.log = Log(debug)

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

        :param volume_id:
        :return:
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

    def create(self, name, driver, driver_opts, labels):
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
