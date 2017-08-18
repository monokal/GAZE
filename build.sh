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
    echo -e "\n[GAZE] Docker is required to build GAZE. Please install it then try again.\n"
    exit 1
fi

echo -e "\n[GAZE] Building & pushing the gazectl Docker Image...\n"
cd gaze-control && ./gazectl-build.sh; cd -

echo -e "\n[GAZE] Building & pushing documentation...\n"
mkdocs build --clean && mkdocs gh-deploy

echo -e "\n[GAZE] Pushing all changes to Git...\n"
git add -A && git commit -m "Pushed by ${0}" && git push

echo -e "\n[GAZE] Done!\n"
