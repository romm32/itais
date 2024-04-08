Se tienen dos flowgraphs de GNU Radio. El que se llama "bidireccional1" envía arreglos de dimensión 10 y recibe arreglos de dimensión 2. El flowgraph "bidireccional2" envía arreglos de dimensión 2 y recibe arreglos de dimensión 10. La idea es la misma que en las pruebas para el vector de tamaño 10 (que era unidireccional).

Para ejecutar, se puede correr cualquiera de los dos flowgraphs primero.

**Hay algunos valores de vector_length o num_items que nos parece que no tienen mucho sentido (por ej, en los bloques PUB/SUB, que ni siquiera tienen el mismo valor), pero son los que funcionaron.**
