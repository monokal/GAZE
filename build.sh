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

NAMESPACE=${GAZECTL_NAMESPACE:='monokal'}
IMAGE=${GAZECTL_IMAGE:='gazectl'}
TAG=${GAZECTL_VERSION:='latest'}

PURPLE='\033[0;35m'
NONE='\033[0m'

if ! hash docker 2>/dev/null; then
    echo -e "${PURPLE}[GAZE] Docker is required to build GAZE. Please install it then try again.${NONE}"
    exit 1
fi

# Build & push the gazectl Docker Image.
echo -e "\n${PURPLE}[GAZE] Building & pushing the ${NAMESPACE}/${IMAGE}:${TAG} Docker Image...${NONE}\n"
docker build -t "${NAMESPACE}/${IMAGE}:${TAG}" gaze-control/ && \
docker push "${NAMESPACE}/${IMAGE}:${TAG}"

# Build & deploy documentation.
echo -e "\n${PURPLE}[GAZE] Building & pushing documentation...${NONE}\n"
mkdocs build --clean && mkdocs gh-deploy

# Push all changes to Git.
echo -e "\n${PURPLE}[GAZE] Pushing all changes to Git...${NONE}\n"
git add -A && git commit -m "Pushed by ${0}" && git push

echo -e "\n${PURPLE}[GAZE] Success!${NONE}\n"
