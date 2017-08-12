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

from jinja2 import Environment, FileSystemLoader

from .log import Log


class Template(object):
    """ Provides methods to manage Jinja2 templates. """

    def __init__(self):
        """
        """

        self.log = Log()

    def render(self, template, items, destination):
        """
        Render a Jinja2 template to file.

        :param template: String: Path of the Jinja2 template file.
        :param items: Dict: Values required to render the template.
        :param destination: String: Path of the rendered file.
        """

        self.log("Rendering template ({})...".format(template), 'info')
        try:
            j2_env = Environment(
                loader=FileSystemLoader("/opt/gazectl/templates"),
                trim_blocks=True
            )
            rendered = j2_env.get_template(template).render(items)
            self.log("Rendered template:\n{}".format(rendered), 'debug')

        except Exception as e:
            self.log(
                "Failed to render template ({}) with exception:"
                "\n{}".format(template, e), 'exception'
            )
            sys.exit(1)

        self.log("    * Success!", 'success')

        self.log("Writing template to file ({})...".format(destination), 'info')
        try:
            with open(destination, "w") as file:
                file.write(rendered)

        except Exception as e:
            self.log(
                "Failed to write template to file ({}) with exception:"
                "\n{}".format(destination, e), 'exception'
            )
            sys.exit(1)

        self.log("    * Success!", 'success')
