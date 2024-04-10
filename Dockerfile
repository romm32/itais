FROM ubuntu:20.04
MAINTAINER "Romina García, Máximo Pirri"
# Based on https://github.com/git-artes/docker-gnuradio by Federico La Rocca <flarroca@fing.edu.uy> and https://gitlab.fing.edu.uy/comina/lab-integrador by Gonzalo Belcredi."

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update --fix-missing

# else it will output an error about Gtk namespace not found
RUN apt-get install -y gir1.2-gtk-3.0

# to have add-apt-repository available
RUN apt-get install -y software-properties-common

RUN add-apt-repository main
RUN add-apt-repository universe
RUN add-apt-repository -y ppa:gnuradio/gnuradio-releases-3.8
RUN add-apt-repository ppa:nuandllc/bladerf
RUN apt-get update --fix-missing

# create user gnuradio with sudo (and password gnuradio)
RUN apt-get install -y sudo
RUN useradd --create-home --shell /bin/bash -G sudo gnuradio
RUN echo 'gnuradio:gnuradio' | chpasswd

# I create a dir at home which I'll use to persist after the container is closed (need to change it's ownership)
RUN mkdir /home/gnuradio/persistent  && chown gnuradio /home/gnuradio/persistent

RUN sudo apt-get install -y cmake libusb-1.0 libusb-1.0-0-dev swig

#RUN sudo apt-get install -y rtl-sdr


RUN apt-get install -y git



# Volk
#RUN git clone --recursive https://github.com/gnuradio/volk.git /home/gnuradio/volk/
#RUN cd /home/gnuradio/volk/ && mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/usr/bin/python3 ../ && make && make test && sudo make install && sudo ldconfig


# Install rtl-sdr
RUN sudo apt-get install -y git cmake libusb-1.0 libusb-1.0-0-dev swig pkg-config
RUN git clone https://gitea.osmocom.org/sdr/rtl-sdr.git /home/gnuradio/rtl-sdr/ && cd /home/gnuradio/rtl-sdr/ && mkdir build && cd build && cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON && make && sudo make install && sudo ldconfig 


# Install hackrf
RUN sudo apt-get install -y libhackrf-dev

# Install bladerf

RUN apt-get install -y bladerf
RUN apt-get install -y libbladerf-dev


RUN apt-get install -y python3.9 gnuradio

# Install gr-osmosdr
RUN sudo apt install liborc-0.4-0 liborc-0.4-dev
RUN git clone --branch gr3.8 https://github.com/osmocom/gr-osmosdr.git /home/gnuradio/gr-osmosdr/
RUN cd /home/gnuradio/gr-osmosdr/ && mkdir build && cd build/ && cmake -DCMAKE_INSTALL_PREFIX=/usr ../ && make && sudo make install && sudo ldconfig


# installing other packages needed for downloading and installing OOT modules
RUN apt-get install -y gnuradio-dev cmake git libboost-all-dev libcppunit-dev liblog4cpp5-dev swig liborc-dev libgsl-dev

# of course, nothing useful can be done without vim
RUN apt-get update && apt-get install -y vim 

# of course, nothing useful can be done without pip
RUN apt-get install -y pip 

# of course, nothing useful can be done without tmux
RUN apt-get install -y tmux 

RUN apt remove -y soapysdr0.7-module-remote


# Install PlutoSDR
#RUN apt-get install -y libxml2 libxml2-dev bison flex libaio-dev libavahi-common-dev libavahi-client-dev liborc-dev

#RUN apt-get update && apt-get install -y libzstd-dev
#RUN apt-get update && apt-get install -y libc6-dev
    
#RUN git clone https://github.com/analogdevicesinc/libiio.git /home/gnuradio/libiio
#RUN cd /home/gnuradio/libiio && mkdir build && cd build && cmake .. -DPYTHON_BINDINGS=ON && make && make install

#ENV CMAKE_PREFIX_PATH="/home/gnuradio/libiio"
#ENV LIBIIO_INCLUDEDIR="/home/gnuradio/libiio/include"
#RUN git clone https://github.com/analogdevicesinc/libad9361-iio.git /home/gnuradio/libad9361-iio
#RUN cd /home/gnuradio/libad9361-iio && mkdir build && cd build && cmake -DCMAKE_PREFIX_PATH="/home/gnuradio/libiio" .. -DPYTHON_BINDINGS=ON && make && make install

#RUN git clone -b upgrade-3.8 https://github.com/analogdevicesinc/gr-iio.git /home/gnuradio/gr-iio
#RUN cd /home/gnuradio/gr-iio && cmake . && make && sudo make install
#RUN sudo ldconfig 

#Install gr-ais
# From git
#RUN git clone https://github.com/bistromath/gr-ais.git /home/gnuradio/gr-ais

# From local folder
ADD gr-ais /home/gnuradio/gr-ais

#RUN cd /home/gnuradio/gr-ais && mkdir build && cd build && cmake -DCMAKE_INSTALL_PREFIX=/usr ../ && make && sudo make install
#RUN ldconfig

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 20

#RUN volk_profile
RUN apt-get update
RUN apt-get install -y usbutils gedit

# Install PlutoSDR
RUN apt-get install -y libxml2 libxml2-dev bison flex libaio-dev libavahi-common-dev libavahi-client-dev liborc-dev

RUN git clone https://github.com/analogdevicesinc/libiio.git /home/gnuradio/libiio
RUN cd /home/gnuradio/libiio && git checkout v0.24 && mkdir build && cd build && cmake .. -DPYTHON_BINDINGS=ON && make && make install

RUN git clone https://github.com/analogdevicesinc/libad9361-iio.git /home/gnuradio/libad9361-iio
RUN cd /home/gnuradio/libad9361-iio && mkdir build && cd build && cmake .. -DPYTHON_BINDINGS=ON && make && make install

RUN git clone -b upgrade-3.8 https://github.com/analogdevicesinc/gr-iio.git /home/gnuradio/gr-iio
RUN cd /home/gnuradio/gr-iio && cmake . && make && make install
RUN ldconfig

ADD gr-itais /home/gnuradio/gr-itais
ADD GPS-communication /home/gnuradio/GPS-communication

RUN pip install pyserial
RUN pip install pynmea2
RUN pip install zmq

USER gnuradio

WORKDIR /home/gnuradio

ENV PYTHONPATH "${PYTHONPATH}:/usr/local/lib/python3/dist-packages:/home/gnuradio/gr-ais/python:/home/gnuradio/gr-itais/python:/home/gnuradio/gr-aistx/python"

CMD bash
