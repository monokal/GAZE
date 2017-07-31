![GAZE project logo](docs/raccoon.png "GAZE project")

## What's GAZE?
It's a true turnkey open-source media centre solution. It will deploy, configure and network the following services, making use of Docker's ecosystem:
- **Sonarr**, to manage TV series downloads.
- **Radarr**, to manage movie downloads.
- **Jackett**, to manage torrent trackers.
- **Transmission**, a torrent client.
- **Plex Media Server**, to encode and stream media to devices.
- **PlexPy**, a Plex monitoring dashboard.
- **Ombi**, a unified web-UI for managing Sonarr/Radarr/Plex/etc.
- **cAdvisor**, to provide resource usage and performance metrics of services.

Additionally, to package all of the above in to a user-friendly service, we also provide:
- **GAZE Router**, a proxy service and web-UI to provide easy access to all of the above.
- **GAZE Monitor**, a shiny Grafana dashboard to display the metrics from cAdvisor and other services.
- **GAZE CLI**, a command-line tool to manage the full stack.

## Installation (Linux)
To install the `gaze` command-line tool and deploy the full GAZE stack in one shot, just paste the following in to a shell:
```sh
curl -X GET -H "Content-Type: application/json" https://raw.githubusercontent.com/monokal/GAZE/master/gaze.py > /usr/local/bin/gaze && chmod +x /usr/local/bin/gaze && gaze up
```
On completion, you will be presented with all the details you need to access the services.

## Usage
To make life easy, we provide the `gaze` command-line tool to manage the full stack of services. If you followed the Installation section above, you already have it! Usage can be seen using the following command:
```sh
gaze --help
```

## Issues / Feature Requests
If you experiance any problems, bugs or would like to request a new feature, please first search for duplicates then raise a ticket here: https://github.com/monokal/GAZE/issues

## Contributions
If you'd like to contribute to the GAZE project, simply fork the `master` branch, make and test your changes then open a Pull Request here: https://github.com/monokal/GAZE/pulls
