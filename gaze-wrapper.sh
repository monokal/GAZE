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

NAMESPACE=${GAZE_CLI_NAMESPACE:=monokal}
IMAGE=${GAZE_CLI_IMAGE:=gaze}
TAG=${GAZE_CLI_VERSION:=latest}

if ! hash docker 2>/dev/null; then
    echo 'Docker is required to run GAZE. Please install it then run "gaze init" again.'
    exit 1
fi

docker pull "${NAMESPACE}/${IMAGE}:${TAG}"

# Mount the host Docker daemon's socket so we can manage host containers from
# within the "gaze" container.
docker run \
    -ti \
    --name GAZE \
    -v /var/run/docker.sock:/var/run/docker.sock \
    "${NAMESPACE}/${IMAGE}:${TAG}" \
    "${@}"
