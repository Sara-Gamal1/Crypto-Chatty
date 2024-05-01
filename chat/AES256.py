from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib
from Crypto.Util.Padding import pad, unpad

def encrypt(plain_text, key):
    key=hashlib.sha256(str(key).encode()).digest()
    
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(plain_text, AES.block_size)
    cipher_text = cipher.encrypt(padded_text)
    return base64.b64encode(cipher_text)

def decrypt(cipher_text, key):
    key=hashlib.sha256(str(key).encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_text = cipher.decrypt(base64.b64decode(cipher_text))
    return unpad(decrypted_text,AES.block_size)


# key =42134324

# plaintext = b'This is a secret message.'

# cipher_text = encrypt(plaintext, key)
# print( cipher_text)

# decrypted_text = decrypt(cipher_text, key)
# print("Decrypted:", decrypted_text.decode())

__all__ = ["decrypt", "encrypt"]
