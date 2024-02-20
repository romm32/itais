solo para saber:
antes de correr el docker, es necesario tener en esta carpeta:
-gr-ais bajado desde github con un gitclone:

git clone https://github.com/bistromath/gr-ais.git

-gr-aistx bajado desde github con un gitclone:

git clone -b src-formatting https://github.com/bmagistro/gr-aistx.git

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
