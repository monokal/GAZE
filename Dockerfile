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

FROM python:alpine

# Alpine packages to install.
ENV APK_PACKAGES \
    alpine-sdk \
    libffi-dev \
    openssl-dev \
    tzdata \
    nodejs \
    nginx

# PyPI packages to install.
ENV PIP_PACKAGES \
    docker \
    termcolor \
    jinja2 \
    tabulate \
    pyyaml \
    flask \
    gunicorn

# Install the Alpine packages.
RUN apk --no-cache add $APK_PACKAGES

# Install the above packages, configure system time and create the gazectl directory.
RUN apk --no-cache add $APK_PACKAGES && \
    pip --no-cache-dir install $PIP_PACKAGES && \
    cp /usr/share/zoneinfo/Europe/London /etc/localtime && \
    echo "Europe/London" > /etc/timezone && \
    apk del tzdata && \
    mkdir -p /opt/gazectl

WORKDIR /opt/gazectl
COPY gaze .

# Compile Python source, then remove it.
RUN python -m compileall -b .; \
    find . -name "*.py" -type f -print -delete

ENTRYPOINT ["python", "gazectl.pyc"]
