En esta carpeta se busca ver cómo funciona el bloque de GNU Radio "Python block", que permite definir un bloque de 
GNU Radio desde Python directo. Para esto armamos un esquema muy sencillo en el que una sinusoidal pasa por el 
bloque creado por nosotros, y luego va a un time sink. Al ejecutarlo, se guarda el .grc asociado al flowgraph y
el .py que define el bloque. Esta pruebita nos permite ver cómo se inicializa el bloque de Python en el .py del 
diagrama, y así es que lo vamos a inicializar en el radio.py. Nuestro objetivo es que este bloque de Python sea
el que calcule la potencia y el umbral, y se los envíe al transmisor.
