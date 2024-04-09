En el archivo Prueba_Potumbral.ipynb se encuentra una prueba del código utilizado en radio.py para poder calcular correctamente el umbral y medir la potencia actual del canal. Si bien en este archivo no se tendrán entradas reales en el canal se crean valores complejos para las muestras para corroborar que el cálculo se hace como fue pretendido (y como lo establece la norma).


El código se encuentra comentado indicando cómo es que se crea el archivo con las muestras y cómo funciona la función que crea dicho archivo. En este archivo se explicarán los distintos casos de prueba y cómo los resultados arrojados por cada uno verificaban el funcionamiento deseado o despejaba un posible caso de falla. 


 Caso random: La principal idea de este archivo es verificar que las muestras se van creando y organizando como se pretendía. Al ser los valores complejos aleatorios, no ayuda demasiado a determinar si el cálculo de la potencia es correcto (pues no se sabe a priori cuánto debería valer) y en consecuencia no se le dió mucho más uso.


Caso probar20ms1:  Se inicializa el archivo de muestras con una cantidad dada de líneas, cada una con 1000 muestras (correspondientes a 20 ms). Cada subintervalo de 20ms tendrá un valor 0.1 mayor al anterior (en ambas componentes, compleja y real), iniciando en cero. Nos interesa probar que se calcula de forma correcta el promedio en cada subintervalo de 20 ms. Como cada subintervalo de 20ms tiene el mismo valor, el promedio es conocido (y coincide con el valor de las muestras). Lo que se logra ver en este caso es el valor de 3 intervalos de 20ms distintos en donde siempre se calcula de forma correcta el promedio para cada uno.


Caso probar20ms2: Para ver un caso más general de prueba, se utiliza la misma idea que en la prueba de 20ms anterior pero en este caso lo que se hace es ingresar los primeros 10ms de un valor y los siguientes 10ms de otro valor diferente. Como todos los valores de la primera mitad son iguales y conocidos y los de la segunda también, se puede conocer de antemano el valor del promedio. Esto permite ver que el promedio se esté calculando bien en un caso más general y descartar que por ejemplo se esté tomando la última muestra como el promedio de los últimos 20ms.


Caso probar4s1: En este caso, se desea probar que cuando se llega a una cantidad de muestras que equivalen a 4 segundos, el funcionamiento es el correcto. Para esto, se ingresan 3 intervalos de 4 segundos que equivale a 3x200 subintervalos de 20ms. Cada subintervalo de 20ms tiene el mismo valor en todas sus muestras pero en los siguientes subintervalos que equivalen a 20ms el valor de las muestras aumenta. Esto hace que el valor vaya aumentando desde el primer subintervalo hasta el subintervalo 600. Como el valor de potencia que representa a cada intervalo de 4 segundos es el valor más chico entre los promedios de los 200 subintervalos de 20ms que lo forman, cada intervalo de 4 segundos estará representado por el primer subintervalo de 20ms. Esto se debe a que los siguientes tendrán un valor más grande.






Caso probar4s2: La idea es hacer algo muy similar al caso anterior de 4 segundos. Como en el caso anterior coincidía que el representante de cada intervalo de 4 segundos era el primero de los 200 subintervalos de 20ms, ahora se cambió la forma en que se cargan los intervalos para que esto no sea así. Podría hacerse en orden decreciente, pero en ese caso el representante de cada intervalo de 4 segundos sería el último subintervalo de 20ms de los 200.  Se decidió entonces armar una pirámide invertida, es decir, para los primeros 300 subintervalos de 20ms el valor de las muestras va disminuyendo y para los últimos 300 subintervalos el valor de las muestras va aumentando. Esto hace que en el primer intervalo de 4 segundos, su representante sea el último subintervalo de los 200 que lo forman, en el segundo intervalo de 4 segundos el representante va a ser el del medio y en el tercer intervalo de 4 segundos el representante será el primero de los 200 que lo forman. Como se conoce en qué valor comienzan las muestras y cómo va aumentando, se puede conocer el valor que se espera que represente a cada intervalo y los valores coinciden. 


Caso probar1min: En este caso lo que se quiere probar es que se carguen de forma correcta 15 intervalos de 4 segundos. Esto se hace asegurándonos de que se mantengan constantes los valores de las muestras. Se ve como los valores de 4 segundos se van agregando en el arreglo de los 15 intervalos de forma correcta. Como se toma el mínimo de los 15 intervalos y son inicializados con el menor valor posible de umbral, el valor del umbral se actualiza cuando  se tienen 15 valores nuevos 4 segundos. Los valores de 4 segundos van aumentando, en consecuencia el valor más pequeño de los 15 que forman el minuto será el primero (luego de sacar los 15 con los que se inicializa el arreglo).


Casi probar1min_2: Se desea probar lo mismo que se probó en el caso anterior pero para descartar que siempre se esté tomando el primer valor de 4 segundos de los 15 posibles, se van aumentando los valores de 4 segundos y a partir de cierto momento empiezan a disminuir. Esto hace que los valores más pequeños vayan variando de posición en el arreglo (al aumentar el valor más pequeño es el más viejo del arreglo y cuando empiezan a disminuir pasa a ser el más nuevo).