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

from gazelib.core.log import GazeLog


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

    def run(self, name, image, privileged=False, environment=None,
            volumes=None, network_mode=None, networks=None, ports=None,
            labels=None, cap_add=None, restart_policy=None, command=None):
        """
        Run a Docker Container.
        :param name: (str) The name of the container.
        :param image: (str) The image to run.
        :param privileged: (bool) Give extended privileges to this container.
        :param environment: (dict or list) Environment variables.
        :param volumes: (dict or list) Volumes to mount inside the container.
        :param network_mode: (str) Network mode, incompatible with "networks".
        :param networks: (list) Names of network(s) to connect to.
        :param ports: (dict) Ports to bind inside the container.
        :param restart_policy: (dict) Restart policy of the container.
        :param labels: (dict or list) Labels to set on the container.
        :param cap_add: (list of str) Add kernel capabilities.
        :param command: (str or list) The command to run in the container.
        :return container: (object) A Container object.
        """

        run_options = {
            'name': name,
            'image': image,
            'privileged': privileged,
            'detach': True  # Force otherwise we wont get a Container object.
        }

        # Append optional parameters to the "run" command if provided as we
        # don't want mutable defaults.
        if environment is not None:
            run_options['environment'] = environment
        if volumes is not None:
            run_options['volumes'] = volumes
        if ports is not None:
            run_options['ports'] = ports
        if labels is not None:
            run_options['labels'] = labels
        if cap_add is not None:
            run_options['cap_add'] = cap_add
        if restart_policy is not None:
            run_options['restart_policy'] = restart_policy
        if command is not None:
            run_options['command'] = command

        # Only one of "network_mode" or "networks" can be used. If neither is
        # defined then default to "bridged" as "docker run" usually would.
        if network_mode is not None:
            run_options['network_mode'] = network_mode

        elif networks is not None:
            run_options['network'] = networks[0]

        else:
            run_options['network_mode'] = 'bridged'

        # Run the container using the above "run_options".
        self.log("Creating the {} container...".format(name), 'info')
        try:
            container = self.docker_client.containers.run(**run_options)

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
        # networks using "Network.connect()" once it's created. Skip the first
        # network as we've already added it during creation above.
        if networks is not None:
            if len(networks) > 1:
                for i in networks[1:]:
                    self.log(
                        "Attaching \"{}\" to additional network \"{}\"...".format(
                            name, i), 'info')

                    try:
                        network = self.docker_client.networks.get(i)

                    except docker.errors.NotFound:
                        self.log(
                            "The Docker Network ({}) was not found.".format(
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

        self.log("OK!", 'success')
        return container

    def get(self, name):
        """
        Get a Container object by name or ID.
        :param name: (str) Name or ID of the Container.
        :return: (object) A Container object.
        """

        try:
            container = self.docker_client.containers.get(name)

        except docker.errors.NotFound:
            self.log(
                "The \"{}\" container could not be found.".format(name),
                'exception'
            )
            sys.exit(1)

        except docker.errors.APIError as e:
            self.log(
                "The Docker daemon returned the following error:\n{}".format(
                    e),
                'exception'
            )
            sys.exit(1)

        self.log("Got Container object: {}".format(container), 'debug')
        return container

    def start(self, name):
        """
        Start a container.
        :param name: (str) Name of the Container.
        """

        container = self.get(name)

        try:
            container.start()

        except docker.errors.APIError as e:
            self.log(
                "The Docker daemon returned the following error:\n{}".format(
                    e), 'exception')
            sys.exit(1)

    def stop(self, name):
        """
        Stop a container.
        :param name: (str) Name of the Container.
        """

        container = self.get(name)

        try:
            container.stop()

        except docker.errors.APIError as e:
            self.log(
                "The Docker daemon returned the following error:\n{}".format(
                    e), 'exception')
            sys.exit(1)

    def remove(self, name):
        """
        Remove a container.
        :param name: (str) Name of the Container.
        """

        container = self.get(name)

        try:
            container.remove()

        except docker.errors.APIError as e:
            self.log(
                "The Docker daemon returned the following error:\n{}".format(
                    e),
                'exception'
            )
            sys.exit(1)
