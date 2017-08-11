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

from jinja2 import Environment, FileSystemLoader

from .log import Log


class Template(object):
    """ Provides methods to manage Jinja2 templates. """

    def __init__(self, debug=False):
        """
        :param debug: Boolean: Set the logger to debug verbosity.
        """

        self.log = Log()

    def render(self, template, items, destination):
        """
        Render a Jinja2 template to file.

        :param template: String: Path of the Jinja2 template file.
        :param items: Dict: Values required to render the template.
        :param destination: String: Path of the rendered file.
        """

        self.log("Rendering template ({})...".format(destination), 'info')

        j2_env = Environment(loader=FileSystemLoader("templates"))
        rendered = j2_env.get_template(template).render(items)

        with open(destination, "w") as file:
            file.write(rendered)

        self.log("Rendered template ({}):\n{}".format(destination, rendered),
                 'debug')
