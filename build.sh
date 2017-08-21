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
#          monokal.io

set -e

# Dependencies which should be in PATH.
DEPS=( 'docker' 'mkdocs' )

# Environment variable overrides.
NAMESPACE=${GAZECTL_NAMESPACE:='monokal'}
IMAGE=${GAZECTL_IMAGE:='gazectl'}
TAG=${GAZECTL_VERSION:='latest'}

MAGENTA=$(tput setaf 5)
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
NONE=$(tput sgr 0)

#
# Check for dependencies.
#

for i in "${DEPS[@]}"; do
    if ! hash "${i}" 2>/dev/null; then
        echo -e "${RED}[GAZE] "${i}" is required to build GAZE. Please install it then try again.${NONE}"
        exit 1
    fi
done

#
# Build & push the gazectl Docker Image.
#

echo -e "${MAGENTA}[GAZE] Building & pushing the ${NAMESPACE}/${IMAGE}:${TAG} Docker Image...${NONE}"
docker build -t "${NAMESPACE}/${IMAGE}:${TAG}" gaze-control/ && \
docker push "${NAMESPACE}/${IMAGE}:${TAG}"
echo -e "${GREEN}[GAZE] OK.${NONE}"

#
# Build & deploy documentation.
#

echo -e "${MAGENTA}[GAZE] Copying docs/index.md to README.md...${NONE}"
cp -v docs/index.md README.md
echo -e "${GREEN}[GAZE] OK.${NONE}"

echo -e "${MAGENTA}[GAZE] Building & pushing documentation...${NONE}"
mkdocs build --clean && mkdocs gh-deploy
echo -e "${GREEN}[GAZE] OK.${NONE}"

#
# Push all changes to Git.
#

echo -e "${MAGENTA}[GAZE] Pushing all changes to Git...${NONE}"
git add -A && git commit -m "Pushed by ${0}" && git push
echo -e "${GREEN}[GAZE] OK.${NONE}"

echo -e "${GREEN}[GAZE] Finished.${NONE}"

