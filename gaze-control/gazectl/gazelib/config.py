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

import yaml

from .log import GazeLog


class GazeConfig(object):
    def __init__(self):
        """

        """

        self.log = GazeLog()

    def load(self, path):
        """
        Returns a parsed dictionary from a YAML config file.

        :param path: (str) Path to the YAML config file.
        :return: (dict) The parsed configuration dictionary.
        """

        try:
            config_file = open(path)
            config_dict = yaml.safe_load(config_file)
            config_file.close()

        except Exception as e:
            self.log(
                "Failed to load config file ({}) with exception:\n"
                "{}.".format(path, e), 'exception'
            )
            sys.exit(1)

        return config_dict
