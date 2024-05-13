from hashlib import sha1
import random
import os
import datetime 

from utilities import (
    hash_sha1,
    generateRandomK,
    modInverse,
    powerMod,
    readQ_Alpha,
    computeXa,
    computeYa
   
)



def get_file_creation_time(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # Get the creation timestamp of the file
        creation_timestamp = os.path.getctime(file_path)
        
        # Convert the timestamp to a datetime object
        creation_time = datetime.datetime.fromtimestamp(creation_timestamp)
        
        return creation_time
    else:
        # If the file doesn't exist, return None
        return None

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
    public_file = f"{id}algamal.txt"  
    private_file = f"{id}gamal_private.txt"  
    directory = os.path.isfile(public_file)

    current_date = datetime.datetime.now().date()
 
    if  not directory or     (directory and ((current_date-get_file_creation_time(public_file).date()).days>365)):
        print('creating new files')
        # Save Xa and Ya to the file
        with open(public_file, 'w') as file:
            file.write(str(Ya))

        with open(private_file, 'w') as file:
            file.write(str(Xa))

      
    else :
        
       
        with open(public_file, "r") as file:
          Ya = file.readline().strip() 

        if( Ya.isdigit()):
             Ya = int(Ya) 
        else :
            print('error Ya',Ya) 
        with open(private_file, "r") as file:
          Xa = file.readline().strip() 

        if( Xa.isdigit()):
             Xa = int(Xa) 
        else :
            print('error Ya',Xa) 

    return Xa,Ya

def get_friend_gamal_Yb(id):
    if id=="1":
        friend=2
    elif id=="2" :
        friend=1
    filename = f"{friend}algamal.txt"
    line=''
    while(not line.isdigit())  :
        with open(filename, "r") as file:
            line = file.readline().strip() 

            if( line.isdigit()):
                Yb = int(line) 
           
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


