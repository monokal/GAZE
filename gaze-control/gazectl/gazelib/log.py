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
import sys

from termcolor import colored


class Log(object):
    """ Provides a custom GAZE formatted logger. """

    def __init__(self, debug=False):
        """
        :param debug: Boolean: Set the logger to debug verbosity.
        """

        # Initialise a global logger.
        try:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)

            # We're in Docker, so just log to stdout.
            out = logging.StreamHandler(sys.stdout)
            out.setLevel(logging.DEBUG)
            formatter = logging.Formatter("{} %(message)s".format(
                colored('[GAZE]', 'magenta'))
            )
            out.setFormatter(formatter)
            self.logger.addHandler(out)

            if debug:
                self.logger.setLevel(logging.DEBUG)

        except Exception as e:
            print("Failed to initialise logging with exception:\n{}".format(e))
            sys.exit(1)

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
            level = 'exception'
            colour = 'red'
        else:
            colour = 'red'

        target_method = getattr(self.logger, level)
        target_method(colored(message, colour))
