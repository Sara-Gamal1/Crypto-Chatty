import string

START = ord("a")
CHARSET = string.ascii_lowercase[:16]

def encode_b16(plain):
	encoded = ""
	for c in plain:
		binary = "{0:08b}".format(ord(c))
		encoded += (CHARSET[int(binary[:4], 2)] + CHARSET[int(binary[4:], 2)])
	return encoded


def decode_b16(encoded):
    decoded = ""
    for i in range(0, len(encoded), 2):
        hex_char = encoded[i:i+2]
        binary_char = bin(CHARSET.index(hex_char[0]))[2:].zfill(4) + bin(CHARSET.index(hex_char[1]))[2:].zfill(4)
        decimal_char = int(binary_char, 2)  
        decoded += chr(decimal_char)
    return decoded



def caesar_shift(c, k):
	return CHARSET[(ord(c) + ord(k) - 2 * START) % len(CHARSET)]

def caesar_unshift(c, k):
	return CHARSET[((-(ord(k) - 2 * START)+CHARSET.index(c)) % len(CHARSET))-1]

# flag = "secretkey"
# hint: key is a single letter
# key="secretkey"
# print(ord("h"))
# b16 = encode_b16(flag)
# print(b16)
# enc = ""
# for i, c in enumerate(b16):
# 	enc += caesar_shift(c, key[i % len(key)])
# print(enc)

ciphertext="jikmkjgekjkckjkbknkjlhgekflgkjgekbkfkpknkcklgekfgekbkdlkkjgcgejlkjgekckjkjkigelikdgekfkhligekkkflhligc"

for letter in string.ascii_lowercase:
	key = letter
	dec = ""
	for i, c in enumerate(ciphertext):
		dec += caesar_unshift(c, key[i % len(key)])
	plaintext = decode_b16(dec)
	print("Key is ",key," plaintext is ",plaintext)

# After seeing the results:
# the key is "u" and the decrepted ciphertext is "The enemies are making a move. We need to act fast."

