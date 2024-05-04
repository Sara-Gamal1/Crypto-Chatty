from hashlib import sha1
import random
import os
from utilities import (
    hash_sha1,
    generateRandomK,
    modInverse,
    powerMod,
    readQ_Alpha,
    computeXa,
    computeYa
   
)


# Function to get the digital signature for a message
def getDigitalSignature(M, Xa):
    
    m = hash_sha1((M))  
    
    q, alpha = readQ_Alpha("gamal.txt")

    k = generateRandomK(q)
  
    S1 = powerMod(alpha, k, q)  
  
    kInverse = modInverse(k, q - 1) 
    S2 = (kInverse * (m - Xa * S1)) % (q - 1)
    
    return  S1,  S2

# Function to verify a digital signature
def verifyDigitalSignature(M, S1, S2, Yb):
    m = hash_sha1((M)) 
    q, alpha = readQ_Alpha("gamal.txt")
    V1 = powerMod(alpha, m, q)
    temp1 = powerMod(Yb, S1, q)
    temp2 = powerMod(S1, S2, q)
    V2 = (temp1 * temp2) % q
    return V1 == V2



def generateElgamalKeys(id):
  
    Xa=computeXa("gamal.txt")
    Ya=computeYa(Xa,"gamal.txt")
    filename = f"{id}algamal.txt"  
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # Save Xa and Ya to the file
    with open(filename, 'w') as file:
        # file.write(f"Xa: {Xa}\n")
        file.write(str(Ya))

    return Xa,Ya


def get_friend_gamal_Yb(id):
    if id=="1":
        friend=2
    elif id=="2" :
        friend=1
    filename = f"{friend}algamal.txt"  
    with open(filename, "r") as file:
        line = file.readline().strip()  # Read and strip whitespace
        Yb = int(line)  #
    return Yb

    



###########testing 
# xa=computeXa('gamal.txt')
# xb=computeXa('gamal.txt')
# ya=computeYa(xa,'gamal.txt')
# yb=computeYa(xb,'gamal.txt')

# s1,s2=getDigitalSignature(114785296385,xa)
# print(s1,s2)
# print(verifyDigitalSignature(114785296385,s1,s2,ya))
__all__ = ["getDigitalSignature", "verifyDigitalSignature","generateElgamalKeys","get_friend_gamal_Yb"]


