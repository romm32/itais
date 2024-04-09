organización:

1. hablar del proyecto itais, citar nuestra tesis y nuestro paper tal vez. mencionar que esto es un transmisor que cumple ciertas cosas de la norma. decir que está muy basado en gr-ais y gr-aistx, citarlos y decir que se tomaron sus bloques.

2. dependencies: decir que hay dos opciones, o bajar docker (citar el tutorial) y correrlo dentro del entorno del docker, o bajar todas las dependencias una a una e instalarlo directo en alguna compu.

3. installation: poner los comandos para clonar el gitlab y hacer el build de todo.

4. usage instructions: dar las dos opciones, decir que con el docker es necesario primero hacer lo de sh buiild.sh y lo de run, y que de la otra forma vas directo a los comandos. decir que es necesario correr el script del gps (si no tienen gps, pueden usar no gps module), luego el script del tx con el pluto conectado, y si quieren el script de gr-ais (que hay que descargar aparte) con un rtl sdr extra.


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