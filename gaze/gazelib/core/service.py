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

from .container import GazeContainer
from .log import GazeLog


class GazeServices(object):
    """ Provides methods which wrap service Classes. """

    def __init__(self):
        self.log = GazeLog()

        # Instantiate service objects.
        self.plex = GazePlex()
        # self.transmission = GazeTransmission()
        # self.sonarr = GazeSonarr()
        # self.radarr = GazeRadarr()
        # self.jackett = GazeJackett()
        # self.ombi = GazeOmbi()

    # def get_methods(self):
    #     """
    #     Return a list of all methods of the GazeService class (except built-ins
    #     and helpers).
    #
    #     :return: (list) A list of method names.
    #     """
    #
    #     return [m for m in dir(GazeService) if not m.startswith((
    #         '__'
    #     ))]

    def up(self):
        self.plex.up()
        # self.transmission.up()
        # self.sonarr.up()
        # self.radarr.up()
        # self.jackett.up()
        # self.ombi.up()

    def down(self):
        self.plex.down()
        # self.transmission.down()
        # self.sonarr.down()
        # self.radarr.down()
        # self.jackett.down()
        # self.ombi.down()

    def destroy(self):
        self.plex.destroy()
        # self.transmission.destroy()
        # self.sonarr.destroy()
        # self.radarr.destroy()
        # self.jackett.destroy()
        # self.ombi.destroy()


#
# START - Service Classes.
#

class GazePlex(object):
    """ Provides methods to manage the Plex service. """

    def __init__(self):
        self.log = GazeLog()
        self.container = GazeContainer()

    def up(self):
        """

        :return:
        """

        self.log("Deploying Plex service...", 'info')

        container = self.container.run(
            name="gaze_plex",
            image='plexinc/pms-docker:latest',
            environment=[
                "PLEX_CLAIM=TODO",
                "ADVERTISE_IP=0.0.0.0"
            ],
            volumes={
                '/etc/localtime': {
                    'bind': '/etc/localtime',
                    'mode': 'ro'
                }
            },
            networks=['gaze_internal'],
            ports={
                '32400/tcp': 32400
            },
            restart_policy={
                "Name": "on-failure",
                "MaximumRetryCount": 5
            },
            labels={
                "gaze.service": "plex"
            }
        )

        self.log("Success!", 'success')
        return container

    def down(self):
        """

        :return:
        """

        self.container.stop(name=)

    def destroy(self):
        """

        :return:
        """

        pass

#
# END - Service Classes.
#
