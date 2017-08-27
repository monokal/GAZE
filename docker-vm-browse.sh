#!/usr/bin/env bash

#            GAZE
#  Turnkey Open Media Center
#              __        .-.
#          .-"` .`'.    /\\|
#  _(\-/)_" ,  .   ,\  /\\\/     =o O=
# {(=o^O=)} .   ./,  |/\\\/
# `-.(Y).-`  ,  |  , |\.-`
#      /~/,_/~~~\,__.-`   =O o=
#     ////~    // ~\\
#   ==`==`   ==`   ==`
#     gaze.monokal.io

set -e

DEPS=( 'docker' )

MAGENTA=$(tput setaf 5)
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
NONE=$(tput sgr 0)

for i in "${DEPS[@]}"; do
    if ! hash "${i}" 2>/dev/null; then
        echo -e "${RED}[GAZE] "${i}" is required to use this tool. Please install it then try again.${NONE}"
        exit 1
    fi
done

echo -e "${MAGENTA}[GAZE] The Docker VM's filesystem is mounted at \"/vm\".${NONE}"
docker run --rm -it -v /:/vm alpine:edge sh
