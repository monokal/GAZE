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

NAMESPACE=${GAZECTL_NAMESPACE:='monokal'}
IMAGE=${GAZECTL_IMAGE:='gazectl'}
TAG=${GAZECTL_VERSION:='latest'}
SOCKET=${GAZECTL_SOCKET:='/var/run/docker.sock'}

if ! hash docker 2>/dev/null; then
    echo 'Docker is required to run GAZE. Please install it then run "gaze init" again.'
    exit 1
fi

docker pull "${NAMESPACE}/${IMAGE}:${TAG}"

# Mount the host Docker daemon's socket so we can manage host containers from
# within the "gazectl" container.
docker run \
    --name gazectl \
    -ti \
    --rm \
    -v "${GAZECTL_SOCKET}:/var/run/docker.sock" \
    "${NAMESPACE}/${IMAGE}:${TAG}" \
    "${@}"
