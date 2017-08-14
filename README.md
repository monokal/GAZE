<p align="center">
  <img src="static/images/gaze.png" alt="GAZE"/>
</p>

# GAZE - Turnkey Open Media Centre [![Documentation Status](https://readthedocs.org/projects/gaze/badge/?version=latest)](http://gaze.readthedocs.io/en/latest/?badge=latest)
## What's GAZE?
It's a true turnkey open-source media centre solution. It will deploy, configure and network the following services, making use of Docker's ecosystem:
- `Sonarr`, to manage TV series downloads.
- `Radarr`, to manage movie downloads.
- `Jackett`, to manage torrent trackers.
- `Transmission`, a torrent client.
- `Plex Media Server`, to encode and stream media to devices.
- `PlexPy`, a Plex monitoring dashboard.
- `Ombi`, a unified web-UI for managing Sonarr/Radarr/Plex/etc.
- `Prometheus`, to provide resource usage, performance metrics and alerts for services.

Additionally, to aggregate all of the above in to a single user-friendly service, we also provide:
- `GAZE Web`, a proxy service and web-UI to provide easy access to all of the above.
- `GAZE Monitor`, a Grafana dashboard to display service metrics and alerts.
- `GAZE Control`, a command-line tool to manage the full stack.

## Installation (Linux)
Although GAZE should run on any system with Docker, we test builds on **Ubuntu 16.04 LTS and later** so suggest it as a known good configuration.

To install the `gaze` command-line tool and deploy the full media centre stack simply paste the following command into a shell. On completion, you will be presented with all the details you need to access your services:
```sh
curl -L https://raw.githubusercontent.com/monokal/GAZE/master/gaze-control/gazectl-wrapper.sh > /usr/local/bin/gaze && chmod +x /usr/local/bin/gaze && gaze bootstrap
```
If you hit a `Permission denied` error, use `sudo -i` then retry the above command.

**That's it!**
## Usage
To make life easy, the `gaze` command-line tool can be used to manage the full stack of media centre services. Usage can be seen using the following command:
```sh
gaze --help
```
The `gaze` command-line tool also supports overriding various default runtime arguments using environment variables. Sane defaults have been chosen so you shouldn't need to, but if you do:
- `GAZECTL_NAMESPACE` - The Docker Namespace of the `gazectl` container (default: `monokal`).
- `GAZECTL_IMAGE` - The Docker Image of the `gazectl` container (default: `gazectl`).
- `GAZECTL_VERSION` - The Docker Image Tag of the `gazectl` container (default: `latest`).
- `GAZECTL_SOCKET` - The Docker socket of the host (default: `/var/run/docker.sock`).
- `GAZECTL_VOLUMES` - Path to the Docker Volumes mountpoint on the host (default: `/var/lib/docker/volumes`).

## Issues / Feature Requests
If you experience any problems, bugs or would like to request a new feature, please first search for duplicates then raise a ticket here: https://github.com/monokal/GAZE/issues

## Contributions
If you'd like to contribute to the GAZE project, simply fork the `master` branch, make and test your changes then open a Pull Request here: https://github.com/monokal/GAZE/pulls

## Disclaimer
The maintainer(s) of the GAZE project do not advocate the illegal sharing of media in any way. The GAZE project is intended to be an educational programming exercise, and therefore the maintainer(s) assumes no responsibility of improper use.
