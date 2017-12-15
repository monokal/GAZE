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

from .log import GazeLog


class GazeContainer(object):
    """ Provides methods to interact with Docker Containers. """

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

    def run(self, name, image, environment, volumes, networks, ports,
            restart_policy, labels):
        """
        Run a Docker Container.

        :param name: (str) The name of the container.
        :param image: (str) The image to run.
        :param environment: (dict or list) Environment variables.
        :param volumes: (dict or list) Volumes to mount inside the container.
        :param networks: (list) Names of networks to connect to.
        :param ports: (dict) Ports to bind inside the container.
        :param restart_policy: (dict) Restart policy of the container.
        :param labels: (dict or list) Labels to set on the container.
        :return logs: (object) A Container object.
        """

        try:
            container = self.docker_client.containers.run(
                name=name,
                image=image,
                environment=environment,
                volumes=volumes,
                network=networks[0],  # Additional networks are handled below.
                ports=ports,
                restart_policy=restart_policy,
                labels=labels,
                detach=True  # Forced or we wont return a Container object.
            )

        except docker.errors.ContainerError:
            self.log(
                "The {} container exited with a non-zero exit code.".format(
                    name), 'exception')
            sys.exit(1)

        except docker.errors.ImageNotFound:
            self.log(
                "The {} image could not be found.".format(image), 'exception'
            )
            sys.exit(1)

        except docker.errors.APIError as e:
            self.log(
                "The Docker daemon returned the following error:\n{}".format(
                    e),
                'exception'
            )
            sys.exit(1)

        # If more than network was provided, attach the container to additional
        # networks using "Network.connect()" once it's running. Skip the first
        # network as we've already added it during run.
        if len(networks) > 1:
            for i in networks[1:]:
                self.log(
                    "Connecting \"{}\" to additional network \"{}\"...".format(
                        name, i), 'info')

                try:
                    network = self.docker_client.networks.get(i)

                except docker.errors.NotFound:
                    self.log("The Docker Network ({}) was not found.".format(
                        i), 'exception'
                    )
                    sys.exit(1)

                except docker.errors.APIError as e:
                    self.log(
                        "The Docker daemon returned the following error:\n"
                        "{}".format(e), 'exception'
                    )
                    sys.exit(1)

                try:
                    network.connect(container)

                except docker.errors.APIError as e:
                    self.log(
                        "The Docker daemon returned the following error:\n"
                        "{}".format(e), 'exception'
                    )
                    sys.exit(1)

        return container

    def stop(self, name):
        pass
        # TODO: Dafuq is there no stop method?
        # self.docker_client.containers.stop()

    def rm(self):
        pass
