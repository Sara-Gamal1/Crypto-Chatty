import random
import math
from hashlib import sha1


# Function to read q and alpha from a file
def readQ_Alpha(fileName):
    # Assuming you're hardcoding these values instead of reading from a file
    q = 29  # Example value for q
    alpha = 2  # Example value for alpha
    return q, alpha

# Function to convert decimal to binary
def decimalToBinary(decimal):
    return bin(decimal)[2:]  # Convert decimal to binary and remove '0b'

# Function to find modular inverse
def modInverse(a, m):
    for x in range(1, m):
        if ((a % m) * (x % m)) % m == 1:
            return x
    return None

# Function to compute GCD
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Function to generate SHA1 hash and convert it to decimal
def hash_sha1(message):
    hash_object = sha1(message.encode('utf-8'))
    hex_hash = hash_object.hexdigest()  # Hexadecimal representation
    decimal_hash = int(hex_hash, 16)  # Convert hexadecimal to decimal
    return decimal_hash

# Function to generate a random integer K with specific conditions
def generateRandomK(q):
    while True:
        K = random.randint(1, q - 1)  # Generate random integer
        if gcd(K, q - 1) == 1:  # Ensure GCD is 1
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
    "gcd",
    "hash_sha1",
    "generateRandomK",
    "powerMod",
    "computeXa",
    "computeYa",
]
