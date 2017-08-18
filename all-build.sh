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

if ! hash docker 2>/dev/null; then
    echo 'Docker is required to build GAZE. Please install it then try again.'
    exit 1
fi

mkdocs build --clean && mkdocs gh-deploy
cd gaze-control && ./gazectl-build.sh; cd -
