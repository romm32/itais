# Persistent folder

Most of this project was developed inside a Docker environment. This meant that all data that wasn't specifically saved would be lost. For this reason, a _persistent_ folder (conveniently called "Persistent") was created. In this folder, you will find the code and flowgraphs for modular tests we ran. 

A few disclaimers:

1. The code is written in Python. It is very likely that the variable names or the comments in the code are written in Spanish. Should you have any questions, do not hesitate to contact us.

2. Each folder is related to a specific test. A short and simple README file (called "comousar"; "how to use") can be found in every folder, also written in Spanish.

3. Most of these tests were written and run in the first stages of our project. Some tests rely on earlier versions of scripts or blocks inside the _gr-itais_ folder. That being said, the code may not work anymore. You can check below a list of the tests that should still be working.

**Functional tests**
- CalibracionSDR, used to calibrate the ADALM-PLUTO device in comparison to a spectrum analyzer. 
- DemoGMSK, used to understand better the GMSK modulation scheme.
- Prueba_Messages, used to test an early version of the "Messages" block.
- Prueba_Potumbral, used to test an early version of the "Potumbral" block.
- Prueba_Sub_gps, used to test an early verison of the "Sub_GPS" block.
- Prueba_bloqueGNU, used to test GNU Radio's "Python block".
- Pruebas_Elevar2, used to compare Potumbral's computation of instant power of samples to GNU Radio's "Complex to Mag2" block.
- Pruebas_GPS, used to test communication with GPS modules.
- Pruebas_Pasaje_arreglos, used to test GNU Radio's sending and receiving of Python arrays.
- Pruebas_Pasaje_diccionarios, used to test GNU Radio's sending and receiving of Python dictionaries.
- Pruebas_Pluto, used to test using both a Pluto Sink and Pluto Source block in the same GNU Radio flowgraph.
- Pruebas_Pub-Sub, used to test GNU Radio's "ZMQ PUB" and "ZMQ SUB" blocks.
- Pruebas_sensado, used to test Potumbral's sensing in the correct time interval.
- Pruebas_Transmitter, used to test an early verison of the "Transmitter" block.


