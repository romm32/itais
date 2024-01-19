Se tienen dos flowgraphs de GNU Radio. El que se llama "pruebitasPUB" tiene un Python block escrito por nosotros que genera un arreglo de 10 valores y lo envía a través de su salida. Ese vector pasa por un bloque "vector to stream" que lo pasa a un stream de datos, y luego se publica esa información en un bloque ZMQ PUB. El flowgraph "pruebasub" tiene un bloque SUB que recibe el stream del otro flowgraph, lo pasa a un "stream to vector", y nuestro bloque de Python imprime el vector recibido.

Para ejecutar, se puede correr cualquiera de los dos flowgraphs primero.

**Hay algunos valores de vector_length o num_items que nos parece que no tienen mucho sentido (por ej, en los bloques PUB/SUB, que ni siquiera tienen el mismo valor), pero son los que funcionaron.**
