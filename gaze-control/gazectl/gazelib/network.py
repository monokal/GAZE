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

from .error import *
from .log import GazeLog


class GazeNetwork(object):
    """ Provides methods to interact with Docker Network. """

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

    def get(self, network_id):
        """
        Get information about a Docker Network.

        :param network_id: String: ID of the Docker Network.
        :return volume: Docker Network object.
        """

        try:
            network = self.docker_client.networks.get(
                network_id=network_id
            )

        except docker.errors.NotFound:
            self.log(
                "The Docker Network ({}) does not already exist.".format(
                    network_id), 'info'
            )
            raise GazeNetworkNotFound

        except docker.errors.APIError:
            self.log(
                "Failed to get Docker Network ({}).".format(network_id),
                'info'
            )
            sys.exit(1)

        return network

    def create(self, name, driver='local'):
        """
        Create a Docker Network.

        :param name: (str) Name of the Docker Network.
        :param driver: (str) Name of the Network driver.
        :return: A Network object.
        """

        self.log("Creating Docker Network ({})...".format(name), 'info')

        try:
            network = self.get(name)
            self.log(
                "The Docker Network ({}) already exists.".format(name), 'info'
            )

        except GazeNetworkNotFound:
            try:
                network = self.docker_client.networks.create(
                    name=name,
                    driver=driver,
                    labels={"gaze.network": name}
                )

            except docker.errors.APIError:
                self.log(
                    "Failed to create Docker Network ({}).".format(name),
                    'exception'
                )
                sys.exit(1)

        self.log("    * Success!", 'success')

        self.log("Got Docker Network:\n{}".format(network.attrs), 'debug')
        return network
