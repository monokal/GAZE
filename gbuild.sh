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
#     gaze.monokal.io

set -e

function print_usage {
    cat <<EOF
usage: gbuild [-h] {build,test,push,all} ...

GAZE build tool.

positional arguments:
  {build,test,push,all}
    build               build the gazectl Docker Image and documentation
    test                test gazectl functionality
    push                push the gazectl Docker Image, documentation and code
    all                 do all of the above in that order

optional arguments:
  -h, --help            show this help message and exit
EOF
}

function check_deps {
    # Dependencies which should be in PATH.
    DEPS=( 'docker' 'mkdocs' )

    for i in "${DEPS[@]}"; do
        if ! hash "${i}" 2>/dev/null; then
            echo -e "${RED}[GBUILD] "${i}" is required to build GAZE. Please install it then try again.${NONE}"
            exit 1
        fi
    done
}

function run_build {
    # Build Docker Image.
    echo -e "${MAGENTA}[GBUILD] Building the ${NAMESPACE}/${IMAGE}:${TAG} Docker Image...${NONE}"
    docker build -t "${NAMESPACE}/${IMAGE}:${TAG}" gaze-control/
    echo -e "${GREEN}[GBUILD] OK.${NONE}"

    # Copy docs/index.md to README.md
    echo -e "${MAGENTA}[GBUILD] Copying docs/index.md to README.md...${NONE}"
    cp -v docs/index.md README.md
    echo -e "${GREEN}[GBUILD] OK.${NONE}"

    # Build docs.
    echo -e "${MAGENTA}[GBUILD] Building documentation...${NONE}"
    mkdocs build --clean
    echo -e "${GREEN}[GBUILD] OK.${NONE}"
}

function run_test {
    echo -e "${MAGENTA}[GBUILD] Running tests...${NONE}"

    GAZECTL_COMMANDS=( \
        'bootstrap --noup' \
        'up' \
        'down' \
        'status' \
    )

    for i in "${GAZECTL_COMMANDS[@]}"; do
        GAZECTL_VERSION="${TAG}" GAZECTL_UPDATE=${UPDATE} gaze-control/gazectl-wrapper.sh ${i}
    done

    echo -e "${GREEN}[GBUILD] OK.${NONE}"
}

function run_push {
#    # Push Docker Image.
#    echo -e "${MAGENTA}[GBUILD] Pushing the ${NAMESPACE}/${IMAGE}:${TAG} Docker Image...${NONE}"
#    docker push "${NAMESPACE}/${IMAGE}:${TAG}"
#    echo -e "${GREEN}[GBUILD] OK.${NONE}"

    # Push docs.
    echo -e "${MAGENTA}[GBUILD] Pushing documentation...${NONE}"
    mkdocs gh-deploy
    echo -e "${GREEN}[GBUILD] OK.${NONE}"

    # Push everything else.
    echo -e "${MAGENTA}[GBUILD] Pushing all changes to Git...${NONE}"
    git add -A && git commit -m "Pushed by gbuild." && git push
    echo -e "${GREEN}[GBUILD] OK.${NONE}"

    echo -e "${MAGENTA}[GBUILD] The ${NAMESPACE}/${IMAGE}:latest Docker Image will be built automatically by Docker Hub on successful merge.${NONE}"
}

# Environment variable overrides.
export NAMESPACE=${GAZECTL_NAMESPACE:='monokal'}
export IMAGE=${GAZECTL_IMAGE:='gazectl'}
export TAG=${GAZECTL_VERSION:='latest'}
export UPDATE=${GAZECTL_UPDATE:=false} # Default false as we're probably building locally.

MAGENTA=$(tput setaf 5)
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
NONE=$(tput sgr 0)

check_deps

case $1 in
    build)
        run_build
        ;;
    test)
        run_test
        ;;
    push)
        run_push
        ;;
    all)
        run_build
        run_test
        run_push
        ;;
    *)
        print_usage
        exit 1
esac

echo -e "${GREEN}[GBUILD] Finished.${NONE}"
