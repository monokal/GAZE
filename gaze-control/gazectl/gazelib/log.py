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

import logging

from termcolor import colored


class GazeLog(object):
    """ Provides a custom GAZE formatted logger. """

    def __init__(self, logger_name='gaze'):
        """
        :param logger_name: String: Name of the logger object to use.
        """

        self.logger = logging.getLogger(logger_name)

    def __call__(self, message, level, prompt=True):
        """
        :param message: (str) The message to log.
        :param level: (str) Level of the log message from success info,
                      warning, exception, debug.
        :param prompt: (bool) Prepend a fancy unicode icon to the message.
        """

        # Unicode "prompt" characters:
        #     https://en.wikibooks.org/wiki/Unicode/List_of_useful_symbols

        # INFO
        if level == 'info':
            colour = 'cyan'
            prompt = '\u25C9'  # Fish-eye.

        # WARNING
        elif level == 'warning':
            colour = 'yellow'
            prompt = '\u2620'  # Skull and crossbones.

        # DEBUG
        elif level == 'debug':
            colour = 'magenta'
            prompt = '\u25C9'  # Fish-eye.

        # SUCCESS
        elif level == 'success':
            level = 'info'
            colour = 'green'
            prompt = '    \u2714 '  # Heavy check mark.

        # EXCEPTION
        elif level == 'exception':
            colour = 'red'
            prompt = '\u2620'  # Skull and crossbones.

        # If we don't recognise the level, format it as an exception.
        else:
            colour = 'red'
            prompt = '\u2620'  # Skull and crossbones.

        if not prompt:
            prompt = ''

        target_method = getattr(self.logger, level)

        target_method(
            colored(
                " {} {}".format(prompt, message),
                colour
            )
        )
