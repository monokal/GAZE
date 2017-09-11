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
                 ''', 'blue')

        return banner
