# ITAIS project: Implementing a lowcost AIS transceiver using SDR technology
This Gitlab repository contains the implementation of an AIS transceiver _out of tree_ module for GNU Radio 3.8. The project was carried out within the framework of the thesis of authors Romina García and Máximo Pirri, undergraduate students in the Faculty of Engineering of the University of the Republic. The software development is based on the ITU-R M.1371-5 specification for the Automatic Identification System (AIS) technology. Not all requirements are met. The detailed process of implementation, including functionalities, tests and results can be found in the documentation for the project (which will shortly be available online and referenced here). The thesis, as well as most of the comments in this Gitlab repository, are written in Spanish. Should anyone have any question, please do not hesitate to contact the authors.

This project features new blocks created within the ITAIS project, as well as blocks or scripts previously available in other open source projects. Specifically, the general format of scripts and blocks uses [gr-ais](https://github.com/bistromath/gr-ais) as reference, including some unmodified code from said repository. Blocks and scripts from [a GNU Radio 3.8 version of gr-aistx](https://github.com/bmagistro/gr-aistx/tree/src-formatting) are also modified and used. New blocks were written in Python (_Transmitter, Messages, Sub_GPS, Potumbral_) or adapted in C++ (such as a modified version of the GNU Radio 3.9 _Selector_ block, that was inserted into GNU Radio 3.8). 

## Dependencies
### Software requirements
Most of the development was done inside a Docker environment. The Dockerfile, as well as the _build_ and _run_ scripts, can be found in this repository. Working inside de Docker environment is called "Option 1" from now on in this documentation. This option requires no dependencies but to have [installed Docker](https://docs.docker.com/engine/install/) and have followed [the post installation steps](https://docs.docker.com/engine/install/linux-postinstall/). Users can also choose to test the code outside of a Docker environment. This will be referred to as "Option 2". Several dependencies need to be installed in order for everything to work smoothly. These dependencies are described, as well as installation references, in the "Option2_dependencies" file.

### Hardware requirements
There are no specific hardware requirements for the computer in which this code is running. However, we detail the devices in which the code was tested and presented good results. The best results were obtained using an Intel NUC with an i3 processor. This computer also had 16 GB of RAM memory and a 200 GB SSD disk. The module was also tested on a Raspberry Pi 4 Model B with 8 GB of RAM. The code worked well on both computers, but performance was slightly better in the Intel NUC.

It is worth noting that an SDR device for transmission is needed, along with an extra SDR dongle if reception of messages wants to be carried out. The project was tested using an ADALM-PLUTO device for transmission and all following commands imply its usage. It is the only transmission SDR currently supported. This could be easily adapted in the _itais_radio_ script and you are encouraged to do so if you want to test the module using other SDR devices. As for reception, the code used is straight from the _gr-ais_ repository. This allows for use of RTL SDR dongles (which were used during testing of the module), along with other devices specified in their _radio_ script. 

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

`sh build.sh`

4. Run the Docker environment.

`sh run.sh`

5. The first time you use the Docker environment, you need to build the _gr-itais_ module. For this step, you need to use the _build_ folder that is already in this repository. The paths are correct for the Docker environment.

cd gr-itais
cd build

### Option 2
1. Once all the detailed dependencies in the "Option2_dependencies" file have been installed, this repository should be cloned.
`git clone https://gitlab.fing.edu.uy/rominag/itais`


## Usage instructions

4. usage instructions: dar las dos opciones, decir que con el docker es necesario primero hacer lo de sh buiild.sh y lo de run, y que de la otra forma vas directo a los comandos. decir que es necesario correr el script del gps (si no tienen gps, pueden usar no gps module), luego el script del tx con el pluto conectado, y si quieren el script de gr-ais (que hay que descargar aparte) con un rtl sdr extra.

## Contact information
You can use the "Issues" section of this Gitlab repository to post any trouble you might find while trying to use this module. You can also email the authors to the following email addresses: rominag@fing.edu.uy (Romina García) and mpirri@fing.edu.uy (Máximo Pirri). Contact can be done in Spanish, English or German.




después:
-la carpeta persistent se hace sola cuando se corre el build del docker.
-la carpeta gr-itais hay que crearla como un modulo oot de gnuradio. pero 
para que todos los paths esten como tienen que estar, creo que hay que crearla
desde adentro del docker. ADEMAS, no funciona crearla desde afuera porque
no tenemos gnu radio instalado afuera. Lo mejor me parece bajarla directo 
desde un repositorio de github también (que nosotros tenemos que crear).
Así, después se hace el build y el run considerando que esa carpeta es 
permanente y todos los bloques que creemos se van guardando lo más bien.
NOTA: cuando la tuve que crear por primera vez, entré al docker, corrí
el siguiente comando

gr_modtool newmod itais

y eso crea una carpeta que se llama gr-itais. la moví para adentro de 
persistent (para que me apareciera afuera del docker en el sistema de 
archivos) y después la saqué de persistent y la puse en itais como carpeta
externa. creo que no habría necesidad de volver a hacer esto en el futuro.
por las dudas escribí la nota.

aclarar que no hay interfaz grafica para los bloques.
las carpetas que no se tocaron son: docs, grc. esas tienen cosas de nuestro proyecto pero nosotros no las modificamos