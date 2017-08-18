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

set -e

if ! hash docker 2>/dev/null; then
    echo 'Docker is required to build GAZE. Please install it then try again.'
    exit 1
fi

echo "\nBuilding & pushing the gazectl Docker Image...\n"
cd gaze-control && ./gazectl-build.sh; cd -

echo "Building & pushing documentation..."
mkdocs build --clean && mkdocs gh-deploy

echo "\nPushing all changes to Git...\n"
git add -A && git commit -m "Pushed by ${0}" && git push

echo "\nDone!\n"