#               GAZE
#     Turnkey Open Media Centre
#                 __        .-.
#             .-"` .`'.    /\\|
#     _(\-/)_" ,  .   ,\  /\\\/     =o O=
#    {(=o^O=)} .   ./,  |/\\\/
#    `-.(Y).-`  ,  |  , |\.-`
#         /~/,_/~~~\,__.-`   =O o=
#        ////~    // ~\\
#      ==`==`   ==`   ==`
#             monokal.io

NAMESPACE ?= monokal
IMAGE ?= gazectl
TAG ?= latest

.PHONY: all build test docs release

all: build

build:
	docker build -t $(NAMESPACE)/$(IMAGE):$(TAG) gaze-control/

test:
	env NAME=$(NAME) VERSION=$(VERSION) ./test/runner.sh

docs:


release: test
	@if ! docker images $(NAME) | awk '{ print $$2 }' | grep -q -F $(VERSION); then echo "$(NAME) version $(VERSION) is not yet built. Please run 'make build'"; false; fi
	docker push $(NAME)
	@echo "Motherfucker yeah!"
