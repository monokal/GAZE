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

# Environment variable overrides.
NAMESPACE=${GAZECTL_NAMESPACE:='monokal'}
IMAGE=${GAZECTL_IMAGE:='gazectl'}
TAG=${GAZECTL_VERSION:='test'}
SOCKET=${GAZECTL_SOCKET:='/var/run/docker.sock'}
VOLUMES=${GAZECTL_VOLUMES:='/var/lib/docker/volumes'}

DEPS=( 'docker' 'gaze' )

MAGENTA=$(tput setaf 5)
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
NONE=$(tput sgr 0)

for i in "${DEPS[@]}"; do
    if ! hash "${i}" 2>/dev/null; then
        echo -e "${RED}[GAZE] "${i}" is required to build GAZE. Please install it then try again.${NONE}"
        exit 1
    fi
done

docker build -t "${NAMESPACE}/${IMAGE}:${TAG}" gaze-control/

GAZECTL_VERSION="${TAG}" gaze bootstrap --noup
