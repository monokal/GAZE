![GAZE project logo](docs/raccoon.png "GAZE project")

## What is it?
GAZE is a true turnkey open-source media centre solution. It will deploy, configure and pipe together the following services, making use of Docker's ecosystem:
- Sonarr, to manage TV series downloads.
- Radarr, to manage movie downloads.
- Transmission, a torrent client.
- Plex Media Server, to encode and stream your media to devices.
- PlexPy, a Plex monitoring dashboard.
- Ombi, a single web-UI to tie all of the above together.

## Installation (Linux)
To install the `gaze` command-line tool and deploy the full GAZE stack in one shot, just paste the following in to a shell:
```sh
curl -X GET -H "Content-Type: application/json" https://raw.githubusercontent.com/monokal/GAZE/master/gaze.py > /usr/local/bin/gaze && chmod +x /usr/local/bin/gaze && gaze up
```

## Usage
To make life easy, we provide the `gaze` command-line tool to manage the full stack of services. If you followed the Installation section above, you already have it! Usage can be seen using the following command:
```sh
gaze --help
...
```

## Issues / Feature Requests
If you experiance any problems, bugs or would like to request a new feature, please first search for duplicates then raise a ticket here: https://github.com/monokal/GAZE/issues

## Contributions
If you'd like to contribute to the GAZE project, simply fork the `master` branch, make and test your changes then open a Pull Request here: https://github.com/monokal/GAZE/pulls
