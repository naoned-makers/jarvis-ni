#!/bin/sh


export XSOCK=/tmp/.X11-unix
export XAUTH=/tmp/.docker.xauth

xhost +

docker run --dns 192.168.0.1 -d --privileged -v /dev/bus/usb:/dev/bus/usb \
		-v $(pwd):/opt/kinect \
		-v $XSOCK:$XSOCK -v $XAUTH:$XAUTH -e XAUTHORITY=$XAUTH \
		-v /tmp/kinect:/tmp/kinect \
		rguillom/jarvis-ni python src/main.py -H 192.168.0.164

sudo LD_LIBRARY_PATH=/usr/local/lib/ /usr/local/bin/mjpg_streamer -i "input_file.so -f /tmp/kinect -n kinect_jarvis.jpg -d 0,1" -o "output_http.so -w /usr/local/www -p 6660" &
