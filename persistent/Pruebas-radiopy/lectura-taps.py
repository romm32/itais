import numpy as np

# Se abre el archivo generado, se convierten las muestras a complejos y se imprimen.
with open("taps.txt", "rb") as file:
    # Read the bytes from the file
    taps_bytes = file.read()

taps = np.frombuffer(taps_bytes, dtype=np.complex64)
print(taps[:10])

