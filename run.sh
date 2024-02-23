docker run --runtime=runc --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" --privileged --device /dev/snd --device /dev/dri -v /dev/bus/usb/:/dev/bus/usb/ -v $PWD/gr-ais:/home/gnuradio/gr-ais/ -v $PWD/gr-aistx:/home/gnuradio/gr-aistx/ -v $PWD/gr-itais:/home/gnuradio/gr-itais/ -v /var/run/avahi-daemon/socket:/var/run/avahi-daemon/socket --privileged -v $PWD/persistent/:/home/gnuradio/persistent/ --group-add=audio --group-add=plugdev -it ubuntu:ais bash 
