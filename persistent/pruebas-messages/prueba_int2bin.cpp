#include <iostream>

// Function prototype
char *int2bin(int a, char *buffer, int buf_size);

int main() {
    // Example usage
    int number = 4; // You can change this to the desired integer
    const int buffer_size = 33; // Assuming 32 bits for the integer and 1 for null terminator
    char buffer[buffer_size];

    // Convert integer to binary and store in buffer
    char *result = int2bin(number, buffer, buffer_size);

    // Print the binary representation
    std::cout << "Binary representation: " << result << std::endl;

    return 0;
}

// Function definition
char *int2bin(int a, char *buffer, int buf_size) {
    buffer += (buf_size - 1);

    for (int i = 31; i >= 0; i--) {
        *buffer-- = (a & 1) + '0';
        a >>= 1;
    }

    return buffer + 1; // Return the pointer to the beginning of the binary representation
}