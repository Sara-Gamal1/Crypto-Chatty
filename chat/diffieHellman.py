# Assuming you have a Python module called "utilities" with required functions
from utilities import readQ_Alpha, powerMod, computeXa, computeYa

import os

# Define the User class/model (example with MongoDB)
# client = MongoClient("mongodb://localhost:27017/")
# db = client["your_database_name"]
# users_collection = db["users"]

# Async function to update user keys
def generateDiffeHellmanKeys(id):
    Xa = computeXa("diffieHelman.txt")
    Ya = computeYa(Xa, "diffieHelman.txt")
    filename = f"{id}DiffieHellman.txt"  

  
    return Xa,Ya

# Async function to compute secret key
def secretKey(Xa, Yb):
    q, alpha = readQ_Alpha("diffieHelman.txt")
 
   
    if Yb is None or Xa is None:
        raise ValueError("Either Yb or Xa is not defined.")
    K = powerMod(Yb, Xa, q)
    print(q, alpha, Yb, Xa, K)

    return K


##testing
# xa,ya= userKeys()
# xb,yb= userKeys()
# secret_key1 =  secretKey(xa, yb)
# secret_key2 =  secretKey(xb, ya)
# print(secret_key1,secret_key2)

__all__ = ["secretKey", "generateDiffeHellmanKeys"]
