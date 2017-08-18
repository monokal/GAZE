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

SC='\033[0;35m'
EC='\033[0m'

if ! hash docker 2>/dev/null; then
    echo -e "${SC}[GAZE] Docker is required to build GAZE. Please install it then try again.${EC}"
    exit 1
fi

echo -e "\n${SC}[GAZE] Building & pushing the gazectl Docker Image...${EC}\n"
cd gaze-control && ./gazectl-build.sh; cd -

echo -e "\n${SC}[GAZE] Building & pushing documentation...${EC}\n"
mkdocs build --clean && mkdocs gh-deploy

echo -e "\n${SC}[GAZE] Pushing all changes to Git...${EC}\n"
git add -A && git commit -m "Pushed by ${0}" && git push

echo -e "\n${SC}[GAZE] Done!${EC}"
