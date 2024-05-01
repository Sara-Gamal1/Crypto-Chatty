import socket, threading,sys,signal
import binascii
# import apscheduler
# from apscheduler.schedulers.background import BackgroundScheduler
from AES256 import(encrypt,decrypt)
import time
from algamal import (generateElgamalKeys,getDigitalSignature,verifyDigitalSignature,get_friend_gamal_Yb)
from diffieHellman import(generateDiffeHellmanKeys,secretKey)
import base64
from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes
secret_key=0
sharing_key_counter=0
friend_Diffie_Ya=0
friend_s2=0
friend_s1=0
def handle_messages(connection: socket.socket):
    global sharing_key_counter
    global friend_Diffie_Ya
    global friend_s2
    global friend_s1
    while  True:
        try:
            msg = connection.recv(1024)

            # If there is no message, there is a chance that connection has closed
            # so the connection will be closed and an error will be displayed.
            # If not, it will try to decode message in order to show to user.
            if msg:
               
               if(sharing_key_counter>=1):
                    originl_msg=decrypt(msg,secret_key)
                    print(originl_msg.decode())
            sharing_key_counter+=1
            if(sharing_key_counter==1):
               friend_s1, friend_s2, friend_Diffie_Ya = msg.decode().split('|')
               friend_s1=int(friend_s1)
               friend_s2=int(friend_s2)
               friend_Diffie_Ya=int(friend_Diffie_Ya)
            
            else:
                connection.close()
                break

        except Exception as e:
            print(f'Error handling message from server: {e}')
            connection.close()
            break

def client() -> None:
   
    global messages
    global friend_Diffie_Ya
    global friend_s2
    global friend_s1
    SERVER_ADDRESS = '127.0.0.1'
    SERVER_PORT = 12000

    try:
        # Instantiate socket and start connection with server
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))


        initial_msg = socket_instance.recv(1024).decode()

        if "Connection refused" in initial_msg:
            print("Server refused the connection:", initial_msg)
            socket_instance.close()
            return
        # Create a thread in order to handle messages sent by server
       

        print('Connected to chat!')
        id=initial_msg
        gamal_Xa,gamal_Ya=generateElgamalKeys(id)

        Yb= get_friend_gamal_Yb(id)

        Diffie_Xa,Diffie_Ya=generateDiffeHellmanKeys(id)
        s1,s2=getDigitalSignature(Diffie_Ya,gamal_Xa)
        
        
        start = socket_instance.recv(1024).decode()
        print(start)
        threading.Thread(target=handle_messages, args=[socket_instance]).start()

        time.sleep(1)

        print(str(s1),str(s2),str(Diffie_Ya))
        if(id=="2"):
                      
            message = str(s1) + '|' + str(s2) + '|' + str(Diffie_Ya)
            socket_instance.send(message.encode("utf-8"))
            
        if(id=="1"):
            message = str(s1) + '|' + str(s2) + '|' + str(Diffie_Ya)
            socket_instance.send(message.encode("utf-8"))
            



        if(verifyDigitalSignature(friend_Diffie_Ya,friend_s2,friend_s1,Yb)):
            skull="\U0001F480"
            print("There is no evil hacker"+skull)
            secret_key=secretKey(Diffie_Xa,friend_Diffie_Ya)
        else:
            skull="\U0001F480"
            print("You are not my friend,evil hacker"+skull)
            socket_instance.close()
            return
        
        # return     
        # threading.Thread(target=handle_messages, args=[socket_instance]).start()
         

        # Read user's input until it quit from chat and close connection
        while True:
            # scheduler = BackgroundScheduler()
            # scheduler.add_job(generateElgamalKeys, 'interval',days=365,args=( initial_msg))  # Schedule the yearly task
            # scheduler.start()
            msg = input()

            if msg == 'quit':
                break

            # Parse message to utf-8
            
            ciphertext=encrypt(msg.encode('utf-8'),secret_key)
            
            socket_instance.send((ciphertext))

        # Close connection with the server
        socket_instance.close()

    except Exception as e:
        print(f'Error connecting to server socket {e}')
        socket_instance.close()
   


if __name__ == "__main__":
    client()