![GAZE project logo](docs/raccoon.png "GAZE project")

## What is it?
GAZE is a true turnkey open-source media centre solution. It will deploy, configure and pipe together the following services:
- Sonarr, to manage TV series downloads.
- Radarr, to manage movie downloads.
- Transmission, a torrent client.
- Plex Media Server, to encode and stream your media to devices.
- PlexPy, a Plex monitoring dashboard.
- Ombi, a single web-UI to tie all of the above together.

## Installation (Linux)
Just fire up a shell and paste the following:
```sh
curl -X GET -H "Content-Type: application/json" \
https://raw.githubusercontent.com/monokal/GAZE/master/gaze.sh \
> /usr/local/bin/gaze && \
chmod +x /usr/local/bin/gaze && \
gaze up
```

## Usage

## Contribute
