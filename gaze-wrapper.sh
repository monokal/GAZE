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

docker pull "${NAMESPACE}/${IMAGE}:${TAG}" && \
docker run \
    -ti \
    --name GAZE \
    "${NAMESPACE}/${IMAGE}:${TAG}" \
    "${@}"
