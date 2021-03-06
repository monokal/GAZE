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

# Set environment variable defaults.
NAMESPACE=${GAZECTL_NAMESPACE:='monokal'}
IMAGE=${GAZECTL_IMAGE:='gazectl'}
TAG=${GAZECTL_VERSION:='latest'}
SOCKET=${GAZECTL_SOCKET:='/var/run/docker.sock'}
VOLUMES=${GAZECTL_VOLUMES:='/var/lib/docker/volumes'}
PORT=${GAZECTL_PORT:='4293'}
UPDATE=${GAZECTL_UPDATE:=true}

# Ensure we have Docker.
if ! hash docker &>/dev/null; then
    echo 'GAZE > Docker is required to run GAZE. Please install it then try again.'
    exit 1
fi

# Ensure we're running the latest push.
if [ "$UPDATE" = true ] ; then
    docker pull "${NAMESPACE}/${IMAGE}:${TAG}"
fi

# Mount the host Docker daemon's socket so we can manage host containers from
# within the GAZE container, and mount the host's Docker Volumes directory
# so we can bootstrap other services.
docker run \
    --privileged \
    -ti \
    --rm \
    -v "${SOCKET}:/var/run/docker.sock" \
    -v "${VOLUMES}:/var/lib/docker/volumes" \
    -p "${PORT}:4293" \
    "${NAMESPACE}/${IMAGE}:${TAG}" \
    "${@}"
