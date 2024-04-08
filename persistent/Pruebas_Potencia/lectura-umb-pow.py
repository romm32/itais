import numpy as np

# Se abre el archivo generado por el otro script, con los valores de umbral y potencia. Luego se convierten los
# mismos a números complejos o floats para poder imprimirlos.
with open("umbral_y_pow_actual.txt", "rb") as file:
    taps_bytes = file.read()

taps = np.frombuffer(taps_bytes, dtype=np.float64)
print(taps[-10:])


