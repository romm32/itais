En esta carpeta se prueba el bloque "Messages", donde se generan los mensajes 18, 24A y 24B. En este caso, se generan los mensajes como strings de bits, tal como debe recibirlo el siguiente bloque (Build_AIS_Frame) para poder conformar la trama (flags, nrzi, etc) y después enviarla. 

El bloque "Messages" tiene cuatro parámetros que dependen de la embarcación considerada. Parámetros de largo, ancho, tipo y nombre de la misma son modificables por el usuario. 
En el bloque final se cuenta con una entrada de tipo "Mensaje", pero en esta primera versión se tiene una entrada float en su lugar.
A través de esta entrada se recibe el tipo de mensaje que debe generar, 18 (para el mensaje 18), 240 (para el mesaje 24 A) o 241 (para el mensaje 24 B). Cualquier otra entrada no generara un mensaje válido a la salida. 
Se tiene también una entrada de un arreglo de cinco floats. Se recibe un vector con velocidad, longitud, latitud, curso y segundo UTC a colocar en el mensaje. Estos parámetros los recibirá del GPS y son utilizados para la creación de los mensajes.

Se agregaron banderas para evitar que se envíe más de una vez el mismo mensaje al recibir la señal de envío. 
