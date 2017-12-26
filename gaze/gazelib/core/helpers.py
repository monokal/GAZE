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

import socket

from termcolor import colored

from .log import GazeLog


class GazeHelper(object):
    """ Provides general helper methods. """

    def __init__(self):
        self.log = GazeLog()

    @staticmethod
    def ascii_banner():
        banner = colored(r'''
                                 __        .-.
                             .-"` .`'.    /\\|
                     _(\-/)_" ,  .   ,\  /\\\/
                    {(=o^O=)} .   ./,  |/\\\/
                    `-.(Y).-`  ,  |  , |\.-`
                         /~/,_/~~~\,__.-`
                        ////~     //~\\
                      ==`==`    ==`  ==`''', 'magenta')

        banner += colored(r'''
  ██████╗    █████╗   ███████╗  ███████╗
 ██╔════╝   ██╔══██╗  ╚══███╔╝  ██╔════╝
 ██║  ███╗  ███████║    ███╔╝   █████╗  
 ██║   ██║  ██╔══██║   ███╔╝    ██╔══╝  
 ╚██████╔╝  ██║  ██║  ███████╗  ███████╗
  ╚═════╝   ╚═╝  ╚═╝  ╚══════╝  ╚══════╝
   Turnkey Open Media Center
                 ''', 'cyan')

        return banner

    def is_ipv4_address(self, string):
        """
        Check if a string is a valid IPv4 address or not.
        :param string: (str) The string to check IPv4 address validity against.
        :return: (bool) Whether string is a valid IPv4 address or not.
        """

        try:
            socket.inet_aton(string)

        except:
            return False

        return True

    def is_ipv6_address(self, string):
        """
        Check if a string is a valid IPv6 address or not.
        :param string: (str) The string to check IPv6 address validity against.
        :return: (bool) Whether string is a valid IPv6 address or not.
        """

        try:
            socket.inet_pton(socket.AF_INET6, string)

        except:
            return False

        return True
