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


class GazeNetwork(object):
    """ Provides methods to manage Docker Networks. """

    def __init__(self):
        self.log = GazeLog()

        # Instantiate a Docker client.
        try:
            self.docker_client = docker.DockerClient(
                base_url='unix://var/run/docker.sock'
            )

        except docker.errors.APIError:
            self.log("Failed to instantiate a Docker client.", 'exception')
            sys.exit(1)

    def list(self):
        """
        Return all Docker Networks.
        :return networks: List: Docker Network objects.
        """

        try:
            networks = self.docker_client.networks.list()

        except docker.errors.APIError:
            self.log("Failed to get Docker Networks.", 'exception')
            sys.exit(1)

        return networks

    def get(self, network_id):
        """
        Get information about a Docker Network.
        :param network_id: String: ID of the Docker Network.
        :return network: A Network object.
        """

        try:
            network = self.docker_client.networks.get(
                network_id=network_id
            )

        except docker.errors.NotFound:
            raise GazeNetworkNotFound

        except docker.errors.APIError:
            self.log(
                "Failed to get Docker Network ({}).".format(network_id),
                'info'
            )
            sys.exit(1)

        return network

    def create(self, name):
        """
        Create a Docker Network.
        :param name: (str) Name of the Docker Network.
        :return: (object) A Network object.
        """

        try:
            network = self.get(name)
            self.log(
                "The Docker Network ({}) already exists.".format(name), 'info'
            )

        except GazeNetworkNotFound:
            self.log("Creating Docker Network ({})...".format(name), 'info')
            try:
                network = self.docker_client.networks.create(
                    name=name
                )

                self.log("OK!", 'success')

            except docker.errors.APIError:
                self.log(
                    "Failed to create Docker Network ({}).".format(name),
                    'exception'
                )
                sys.exit(1)

        self.log("Got Docker Network:\n{}".format(network.attrs), 'debug')
        return network
