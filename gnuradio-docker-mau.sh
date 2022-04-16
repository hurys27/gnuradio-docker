#!/bin/sh

# Get path of script
TOTEM_FW=$(realpath $(dirname $0))

# Build
#docker build -f ${TOTEM_FW}/docker/Dockerfile.gnuradio -t gnuradio-totem ${TOTEM_FW}/docker/

# Run
xhost + localhost

docker run --rm -it \
       --volume "$(pwd):/home/gnuradio/workdir/" \
       --device /dev/dri:/dev/dri \
       --volume /dev/shm:/dev/shm \
       --volume /tmp/.X11-unix:/tmp/.X11-unix:ro \
       --volume /run/user/$(id -u)/pulse:/run/pulse:ro \
       --volume /var/lib/dbus:/var/lib/dbus \
       --volume /dev/snd:/dev/snd \
       --env USER_UID=$(id -u) \
       --env USER_GID=$(id -g) \
       --env DISPLAY=unix$DISPLAY \
       --hostname gnuradio-totem \
       gnuradio-totem:mau $@
