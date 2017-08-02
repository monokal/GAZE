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

FROM python:3.6.1-alpine

ENV APK_PACKAGES \
    alpine-sdk \
    libffi-dev \
    openssl-dev \
    tzdata

ENV PIP_PACKAGES \
    docker

RUN apk --no-cache add $APK_PACKAGES

RUN apk add tzdata && \
    cp /usr/share/zoneinfo/Europe/London /etc/localtime && \
    echo "Europe/London" > /etc/timezone && \
    apk del tzdata

RUN pip install $PIP_PACKAGES

RUN mkdir -p /opt/gazectl

WORKDIR /opt/gazectl

COPY gazectl .

ENTRYPOINT ["python", "gazectl.py"]
