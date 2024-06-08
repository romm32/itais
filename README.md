# ITAIS project: Implementing a lowcost AIS transceiver using SDR technology
This Github repository contains the implementation of an AIS transceiver _out of tree_ module for GNU Radio 3.8. The project was carried out within the framework of [the thesis of authors Romina García and Máximo Pirri](https://www.colibri.udelar.edu.uy/jspui/handle/20.500.12008/43874), undergraduate students in the Faculty of Engineering of the University of the Republic. This work is also available in the [faculty's Gitlab](https://gitlab.fing.edu.uy/rominag/itais/).

The software development is based on the ITU-R M.1371-5 specification for the Automatic Identification System (AIS) technology. Not all requirements are met. The detailed process of implementation, including functionalities, tests and results can be found in the documentation for the project (which will shortly be available online and referenced here). The thesis, as well as most of the comments in this Gitlab repository, are written in Spanish. Should anyone have any question, please do not hesitate to contact the authors.

This project features new blocks created within the ITAIS project, as well as blocks or scripts previously available in other open source projects. Specifically, the general format of scripts and blocks uses [gr-ais](https://github.com/bistromath/gr-ais) as reference, including some unmodified code from said repository. Blocks and scripts from [a GNU Radio 3.8 version](https://github.com/bmagistro/gr-aistx/tree/src-formatting) of [gr-aistx](https://github.com/trendmicro/ais/tree/master/gr-aistx) are also modified and used. New blocks were written in Python (_Transmitter, Messages, Sub_GPS, Potumbral_) or adapted in C++ (such as a modified version of the GNU Radio 3.9 _Selector_ block, that was inserted into GNU Radio 3.8). Please notice most of the blocks don't have a GUI. They are used in Python scripts that define GNU Radio flowgraphs.

## Dependencies
### Software requirements
This module should be used in a Linux based OS. It was developed and tested in Ubuntu 20.04 and in Raspberry OS (a version from September 2022).

Most of the development was done inside a Docker environment. The Dockerfile, as well as the _build_ and _run_ scripts, can be found in this repository. Working inside the Docker environment is called "Option 1" from now on in this documentation. This option requires no dependencies but to have [installed Docker](https://docs.docker.com/engine/install/) and have followed [the post installation steps](https://docs.docker.com/engine/install/linux-postinstall/). Users can also choose to test the code outside of a Docker environment. This will be referred to as "Option 2". Several dependencies need to be installed in order for everything to work smoothly. These dependencies are described, as well as installation references, in the "Option2_dependencies" file.

### Hardware requirements
There are no specific hardware requirements for the computer in which this code should run. However, we detail the devices in which the code was tested and presented good results. The best results were obtained using an Intel NUC with an i3 processor. This computer also had 16 GB of RAM memory and a 200 GB SSD disk. The module was also tested on a Raspberry Pi 4 Model B with 8 GB of RAM. The code worked well on both computers, but performance was slightly better in the Intel NUC.

It is worth noting that an SDR device for transmission is needed, along with an extra SDR dongle if you want to receive AIS messages. The project was tested using an ADALM-PLUTO device for transmission and all following commands imply its usage. It is the only transmission SDR currently supported. This could be easily adapted in the _itais_radio_ script and you are encouraged to do so if you want to test the module using other SDR devices. As for reception, the code used is straight from the _gr-ais_ repository. This allows for use of RTL SDR dongles (which were used during testing of the module), along with other devices specified in their _radio_ script. 

A NEO-7M GPS module from U-blox was used, along with an active GPS antenna, to obtain GPS data. In the "GPS-communication" folder you will find three scripts to receive GPS data and send it to a TCP socket (which will later be read from the GNU Radio flowgraph). The "get_gps_fast" script was used with the Intel NUC, when the GPS module was connected via USB. The "get_gps_fast_raspi" was used with the Raspberry Pi, when the GPS module was connected using GPIO pins. The "get_gps_no_module" script creates fake GPS data and allows you to test the code without having a GPS module.

## Installation
Installation steps are divided into two, according to the option chosen by the user.

### Option 1 
1. Clone the _itais_ repository.
```
git clone https://gitlab.fing.edu.uy/rominag/itais
cd itais
```

2. Clone the _gr-ais_ repository in the _itais_ folder. This is needed for the Dockerfile to run without issues, even if you don't plan on using an extra RTL SDR for message reception. 

```
git clone https://github.com/bistromath/gr-ais
```

3. Build the Docker environment in the _itais_ folder. This will take a few minutes.

```
sh build.sh
```

4. Run the Docker environment. The username inside is "gnuradio" and the password for sudo is also "gnuradio".

```
sh run.sh
```

5. The _build_ folder is already present in this repository, with the correct paths for the Docker environment. You need to build the module every time you run the Docker environment from scratch, but the _cmake_ command is not needed. The _make_ command will take a little long only the first time you run it (or if you ever modify the files inside the module). If you exit and reopen the Docker, it will take less time.

```
### Inside Docker 
cd gr-itais
cd build
make
sudo make install
sudo ldconfig.
```

6. If you wish to use the receiver from _gr-ais_, you need to build said module from scratch inside the Docker environment. If you exit and reopen the Docker, there is no need to rerun the _cmake_ command.

```
### Inside Docker
cd gr-ais
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig
```

7. Installation is complete. Remember some of the previous steps might be needed again in the future if you exit the Docker environment and reopen it. Please note that **all files that are not inside the _persistent_, the _gr-itais_ or the _gr-ais_ folders will be deleted if you exit the Docker.**

### Option 2
1. Once all the detailed dependencies in the "Option2_dependencies" file have been installed, this repository should be cloned.

```
git clone https://gitlab.fing.edu.uy/rominag/itais

```

2. You need to build the module with the following commands, **having previously deleted the _build_ folder** in this repo.

```
cd itais
cd gr-itais
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig
```

3. If you want to receive AIS messages, you also need to clone the _gr-ais_ repository.

```
cd itais
git clone https://github.com/bistromath/gr-ais
cd gr-ais
mkdir build
cd build
cmake ../
make
sudo make install 
sudo ldconfig 
```

4. Installation is complete.

## Usage instructions
Usage instructions are the same in both options. If you are going to run the code inside the Docker environment, you clearly need to have it running (with the `sh run.sh` command). When testing was carried out, all the commands were run in the same terminal. That means you will need to send some processes to background (Ctrl+Z).  

1. For the transmission flowgraph to work, you need to have opened the TCP socket that receives information from the GPS module. You may choose one of the three scripts present in the _GPS-communication_ folder to do this. If you have a GPS module, connect it to your computer before running the script.

```
python GPS-communication/get_gps_no_module.py
```

2. Run the transmission flowgraph. The ADALM-PLUTO device should already be connected to the computer. 

```
### Inside the itais folder
./gr-itais/apps/itais_radio -s pluto
```

3. If you want to receive AIS messages, you need to have an RTL SDR dongle (or a similar device) connected. Once that is done, the following flowgraph should be run.

```
### Inside the itais folder
./gr-ais/apps/ais_rx -s osmocom
```

## Contact information
You can use the "Issues" section of this Gitlab repository to post any trouble you might find while trying to use this module. You can also email the authors to the following email addresses: rominag@fing.edu.uy (Romina García) and mpirri@fing.edu.uy (Máximo Pirri). Contact can be done in Spanish, English or German.

