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
#          monokal.io

set -e

# Environment variable overrides.
NAMESPACE=${GAZECTL_NAMESPACE:='monokal'}
IMAGE=${GAZECTL_IMAGE:='gazectl'}
TAG=${GAZECTL_VERSION:='latest'}
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

docker run \
    --name gazectl \
    --privileged \
    -ti \
    --rm \
    -v "${SOCKET}:/var/run/docker.sock" \
    -v "${VOLUMES}:/var/lib/docker/volumes" \
    "${NAMESPACE}/${IMAGE}:${TAG}" \
    -d bootstrap --noup

