#!/usr/bin/env bash

#            GAZE
#  Turnkey Open Media Centre
#              __        .-.
#          .-"` .`'.    /\\|
#  _(\-/)_" ,  .   ,\  /\\\/     =o O=
# {(=o^O=)} .   ./,  |/\\\/
# `-.(Y).-`  ,  |  , |\.-`
#      /~/,_/~~~\,__.-`   =O o=
#     ////~    // ~\\
#   ==`==`   ==`   ==`
#          monokal.io

# Set environment variable defaults.
NAMESPACE=${GAZECTL_NAMESPACE:='monokal'}
IMAGE=${GAZECTL_IMAGE:='gazectl'}
TAG=${GAZECTL_VERSION:='latest'}
SOCKET=${GAZECTL_SOCKET:='/var/run/docker.sock'}

# Ensure we have Docker and the Docker daemon socket exists.
if ! hash docker &>/dev/null; then
    echo 'Docker is required to run GAZE. Please install it then run "gaze bootstrap" again.'
    exit 1
fi

if [ ! -S $SOCKET ]; then
    echo "The Docker daemon socket (${SOCKET}) could not be found. Please ensure it's running then run \"gaze bootstrap\" again."
    exit 1
fi

# Always ensure we're running the latest push.
docker pull "${NAMESPACE}/${IMAGE}:${TAG}" &>/dev/null

# Mount the host Docker daemon's socket so we can manage host containers from
# within the "gazectl" container.
docker run \
    --name gazectl \
    -ti \
    --rm \
    -v "${SOCKET}:/var/run/docker.sock" \
    "${NAMESPACE}/${IMAGE}:${TAG}" \
    "${@}"
