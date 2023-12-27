import numpy as np

# Open the file for reading in binary mode
with open("umbral_y_pow_actual.txt", "rb") as file:
    # Read the bytes from the file
    taps_bytes = file.read()

# Convert the bytes back to a NumPy array of complex numbers
taps = np.frombuffer(taps_bytes, dtype=np.float64)
print(taps[-10:])
# Now you can work with the 'taps' array, which contains the complex numbers

