En esta carpeta se tienen todos los bloques necesarios para las primeras pruebas de transmitter.
Se cuenta con algunos bloques que simulan el comportamiento de potumbral.
Otros bloques son utilizados para que comience a operar todo el sistema. Como los bloques que tienen entradas necesitan recibir datos en todas sus entradas para comenzar a operar se crearon bloques que envíen los datos iniciales.

Para poder utilizar esta primera versión de transmitter se debe correr primero bidireccional2.grc.
Ese bloque transmitirá un arreglo de 2 dimensiones a través de un socket, como no tiene entradas puede ejecutarse primero. 
Luego, se debe correr transmitter.grc. En este esquema se recibirán los arreglos de 2 dimensiones y un minuto después se empezarán a enviar arreglos de 10 dimensiones con los candidatos.
Debe dejar de correrse bidireccional2.grc para liberar los sockets donde transmite ese esquema y se debe correr pruebitas.grc.
En dicho esquema se simula el comportamiento de potumbral. Se reciben los 10 slots candidatos y se envía en el socket donde escucha transmitter (donde también mandaba bidireccional2.grc) el slot y si se puede transmitir o no.
Si se puede transmitir en alguno de los slots, en transmitter se le enviará a messages qué mensaje debe enviar e imprime dicha información.
