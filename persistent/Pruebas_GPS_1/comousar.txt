Se tienen varios scripts para comunicación con el módulo GPS, algunos de ellos a través de un FTDI,
otros conectando el módulo a través de pines GPIO y otros para conexión USB. Los scripts finales a utilizar,
que también se encuentran en la carpeta principal, son get_gps_no_module (para usar sin un módulo de GPS), 
get_gps_fast (para usar con el NUC) y get_gps_fast_raspi (para usar con la Raspberry Pi).