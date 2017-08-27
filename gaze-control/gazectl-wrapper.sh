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

# Ensure we have Docker and the Docker daemon socket exists.
if ! hash docker &>/dev/null; then
    echo '[GAZE] Docker is required to run GAZE. Please install it then run "gaze bootstrap" again.'
    exit 1
fi

if [ ! -S ${SOCKET} ]; then
    echo "[GAZE] The Docker daemon socket (${SOCKET}) could not be found. Please ensure it's running then run \"gaze bootstrap\" again."
    exit 1
fi

# Always ensure we're running the latest push.
docker pull "${NAMESPACE}/${IMAGE}:${TAG}" &>/dev/null

# Mount the host Docker daemon's socket so we can manage host containers from
# within the "gazectl" container, and mount the host's Docker Volumes directory
# as we need to bootstrap the "gaze-share" volume.
docker run \
    --name gazectl \
    --privileged \
    -ti \
    --rm \
    -v "${SOCKET}:/var/run/docker.sock" \
    -v "${VOLUMES}:/var/lib/docker/volumes" \
    "${NAMESPACE}/${IMAGE}:${TAG}" \
    "${@}"
