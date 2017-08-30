> _Please note that GAZE is currently under active alpha development and as such is **likely to be in a broken state**._

![GAZE logo](https://raw.githubusercontent.com/monokal/GAZE/master/docs/img/gaze.png "GAZE")

[![Build Status](https://travis-ci.org/monokal/GAZE.svg?branch=master)](https://travis-ci.org/monokal/GAZE) [![Docker Build Status](https://img.shields.io/badge/docker%20build-automated-brightgreen.svg)](https://hub.docker.com/r/monokal/gazectl/) [![GitHub](https://img.shields.io/badge/code-github-blue.svg)](https://github.com/monokal/gaze) [![Chat on Gitter](https://img.shields.io/badge/chat-gitter-blue.svg)](https://gitter.im/gaze-tomc/) [![GPLv3 license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/monokal/GAZE/blob/master/LICENSE) [![Donate via PayPal](https://img.shields.io/badge/donate-paypal-blue.svg)](https://www.paypal.me/monokal/)

## What's GAZE?
It's a true turnkey open-source media center solution. It will deploy, configure and network the following services, making use of Docker's ecosystem:

* [Sonarr](https://sonarr.tv/), to manage TV series downloads.
* [Radarr](https://radarr.video/), to manage movie downloads.
* [Jackett](https://github.com/Jackett/Jackett), to manage torrent trackers.
* [Transmission](https://transmissionbt.com/), a torrent client.
* [Plex](https://www.plex.tv/), to encode and stream media to devices.
* [Ombi](https://github.com/tidusjar/Ombi), a unified web-UI for managing Sonarr/Radarr/Plex/etc.

Additionally, to aggregate all of the above in to a single user-friendly service, we also provide:

* [GAZE Proxy](http://gaze.monokal.io/proxy), a proxy service and web-UI to provide easy access to all of the above.
* [GAZE Monitor](http://gaze.monokal.io/monitor), a Grafana dashboard to display service metrics and alerts.
* [GAZE Control](http://gaze.monokal.io/control), a command-line tool to manage the full stack.

## Installation
Although GAZE should run on any system with Docker, we test builds on **Ubuntu 16.04 LTS and later** so suggest it as a known good configuration.

To install the `gaze` command-line tool and deploy the full media center stack, simply paste the following command into a shell. On completion, you will be presented with all the details you need to access your services:
```bash
curl -L https://raw.githubusercontent.com/monokal/GAZE/master/gaze-control/gazectl-wrapper.sh > /usr/local/bin/gaze && chmod +x /usr/local/bin/gaze && gaze bootstrap
```
If you get a `Permission denied` error, try `sudo -i` then the above command again.

**That's it!**

## Usage
To make life easy, the `gaze` command-line tool can be used to manage the full stack of media center services. Usage can be seen using the following command:
```bash
gaze --help
```
Further documentation on GAZE Control can be [found here](http://gaze.monokal.io/control).

## Documentation
Full documentation on the GAZE project is [available here](http://gaze.monokal.io).

## Support
If you experience any problems, would like to request a new feature or just chat, there are a couple of support channels available:

* [Gitter Chat](https://gitter.im/gaze-tomc/)
* [GitHub Issues](https://github.com/monokal/GAZE/issues)

## Development
If you'd like to contribute to the GAZE project, please read the [development documentation](http://gaze.monokal.io/development).

## Legal
GAZE is released under the [GNU General Public License v3.0](https://github.com/monokal/GAZE/blob/master/LICENSE).
Maintainers of the GAZE project do not advocate the illegal sharing of media in any way, and assume no responsibility for improper use of GAZE or any linked software packages.
By using GAZE, you agree that you will not share or take any action using GAZE that infringes or violates someone else's rights or otherwise violates the law.

> _This `README.md` is overwritten by `docs/index.md` during the build process, so edit that instead._
