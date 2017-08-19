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

# Values which can be overridden using environment variables.
NAMESPACE=${GAZECTL_NAMESPACE:='monokal'}
IMAGE=${GAZECTL_IMAGE:='gazectl'}
TAG=${GAZECTL_VERSION:='latest'}

DEPS=( 'docker' 'mkdocs' )

MAGENTA=$(tput setaf 5)
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
NONE=$(tput sgr 0)

# Check for dependencies.
for i in "${DEPS[@]}"; do
    if ! hash "${i}" 2>/dev/null; then
        echo -e "${RED}[GAZE] "${i}" is required to build GAZE. Please install it then try again.${NONE}"
        exit 1
    fi
done

# Build & push the gazectl Docker Image.
echo -e "\n${MAGENTA}[GAZE] Building & pushing the ${NAMESPACE}/${IMAGE}:${TAG} Docker Image...${NONE}\n"
docker build -t "${NAMESPACE}/${IMAGE}:${TAG}" gaze-control/ && \
docker push "${NAMESPACE}/${IMAGE}:${TAG}"

# Build & deploy documentation.
echo -e "\n${MAGENTA}[GAZE] Building & pushing documentation...${NONE}\n"
mkdocs build --clean && mkdocs gh-deploy

# Push all changes to Git.
echo -e "\n${MAGENTA}[GAZE] Pushing all changes to Git...${NONE}\n"
git add -A && git commit -m "Pushed by ${0}" && git push

echo -e "\n${GREEN}[GAZE] Finished.${NONE}\n"
