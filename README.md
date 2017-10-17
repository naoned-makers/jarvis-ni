# Launch the container

```shell
    ./launch.sh
```

Be carefull : you might need to change the dns IP parameter in the file `launch.sh`
- first get the current DNS IP : 
```shell
  nmcli dev show | grep DNS
```
- and next change the docker `--dns` value

# Stream the images 

**Many thanks to @jacksonliam with the repo https://github.com/jacksonliam/mjpg-streamer !**

## Install the streaming out of the docker img

```shell
    sudo apt-get install cmake libjpeg8-dev

    git  clone git@github.com:jacksonliam/mjpg-streamer.git

    cd mjpg-streamer/mjpg-streamer-experimental
    make
    sudo make install
```

## Usage

```shell
    sudo LD_LIBRARY_PATH=/usr/local/lib/ /usr/local/bin/mjpg_streamer -i "input_file.so -f /tmp/kinect -n kinect_jarvis.jpg -d 0,1" -o "output_http.so -w /usr/local/www -p 8090"
```