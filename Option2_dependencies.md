The following commands are based on the Dockerfile used to develop the module. 

sudo apt-get update --fix-missing

sudo apt-get install -y gir1.2-gtk-3.0

sudo apt-get install -y software-properties-common

sudo add-apt-repository main
sudo add-apt-repository universe
sudo add-apt-repository -y ppa:gnuradio/gnuradio-releases-3.8
sudo add-apt-repository ppa:nuandllc/bladerf
sudo apt-get update --fix-missing

sudo apt-get install -y cmake libusb-1.0 libusb-1.0-0-dev swig
sudo apt-get install -y git

sudo apt-get install -y git cmake libusb-1.0 libusb-1.0-0-dev swig pkg-config
git clone https://gitea.osmocom.org/sdr/rtl-sdr.git /home/gnuradio/rtl-sdr/ && cd /home/gnuradio/rtl-sdr/ && mkdir build && cd build && cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON && make && sudo make install && sudo ldconfig 

sudo apt-get install -y libhackrf-dev
sudo apt-get install -y bladerf
sudo apt-get install -y libbladerf-dev
sudo apt-get install -y python3.9 gnuradio

sudo apt install liborc-0.4-0 liborc-0.4-dev
git clone --branch gr3.8 https://github.com/osmocom/gr-osmosdr.git /home/gnuradio/gr-osmosdr/
cd /home/gnuradio/gr-osmosdr/ && mkdir build && cd build/ && cmake -DCMAKE_INSTALL_PREFIX=/usr ../ && make && sudo make install && sudo ldconfig

sudo apt-get install -y gnuradio-dev cmake git libboost-all-dev libcppunit-dev liblog4cpp5-dev swig liborc-dev libgsl-dev
sudo apt-get install -y pip 
sudo apt-get install -y tmux 
sudo apt remove -y soapysdr0.7-module-remote

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 20

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
