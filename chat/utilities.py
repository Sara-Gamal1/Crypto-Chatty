import random
import math
from hashlib import sha1


# Function to read q and alpha from a file
def readQ_Alpha(fileName):
    
    with open(fileName, "r") as file:
        # Read the first two lines
        first_line = file.readline()
        second_line = file.readline()
        
        # Convert the lines to integers
        Q = int(first_line.strip())  # Strip newline characters
        alpha = int(second_line.strip())
        
        return Q,alpha
    # return 29,2


# Function to convert decimal to binary
def decimalToBinary(decimal):
    return bin(decimal)[2:]  # Convert decimal to binary and remove '0b'



def modInverse(A, M):
    m0 = M
    y = 0
    x = 1
 
    if (M == 1):
        return 0
 
    while (A > 1):
        q = A // M
        t = M
        M = A % M
        A = t
        t = y
        y = x - q * y
        x = t
 
    if (x < 0):
        x = x + m0
 
    return x
 
 

# Function to generate SHA1 hash and convert it to decimal
def hash_sha1(message):
    int_128_bytes = message.to_bytes(16, byteorder='big')  # 16 bytes for 128 bits
    
    sha1_hash =sha1(int_128_bytes)

    sha1_hex = sha1_hash.hexdigest()
    sha1_int = int(sha1_hex, 16)
    return sha1_int


# Function to generate a random integer K with specific conditions
def generateRandomK(q):
    while True:
        K = random.randint(1, q - 1)  # Generate random integer
        if math.gcd(K, q - 1) == 1:  # Ensure math.math.math.gcd is 1
            return K

# Function to compute powerMod (modular exponentiation)
def powerMod(a, b, n):
    result = 1
    binary = decimalToBinary(b)
    for bit in binary:
        result = (result * result) % n  # Square the result
        if bit == "1":
            result = (result * a) % n  # Multiply by 'a' if bit is 1
    return result

# Function to compute Xa
def computeXa(fileName):
    q, alpha = readQ_Alpha(fileName)  # Retrieve q and alpha values
    xa = random.randint(2, q - 3)  # Generate a random Xa value
    return xa

# Function to compute Ya based on Xa
def computeYa(xa,fileName):
    q, alpha = readQ_Alpha(fileName)  # Retrieve q and alpha values
    ya = pow(alpha, xa, q)  # Compute Ya using modular exponentiation
    return ya
__all__ = [
    "readQ_Alpha",
    "decimalToBinary",
    "modInverse",
    "hash_sha1",
    "generateRandomK",
    "powerMod",
    "computeXa",
    "computeYa",
]
