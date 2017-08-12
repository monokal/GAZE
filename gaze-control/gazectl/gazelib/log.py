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

import logging

from termcolor import colored


class GazeLog(object):
    """ Provides a custom GAZE formatted logger. """

    def __init__(self, logger_name='gaze'):
        """
        :param logger_name: String: Name of the logger object to use.
        """

        self.logger = logging.getLogger(logger_name)

    def __call__(self, message, level):
        """
        :param message: String: The message to log.
        :param level: String: Level of the log message from success info,
                      warning, exception, debug.
        """

        if level == 'info':
            colour = 'blue'
        elif level == 'warning':
            colour = 'yellow'
        elif level == 'debug':
            colour = 'magenta'
        elif level == 'success':
            level = 'info'
            colour = 'green'
        elif level == 'exception':
            colour = 'red'
        else:
            colour = 'red'

        target_method = getattr(self.logger, level)
        target_method(colored(message, colour))
