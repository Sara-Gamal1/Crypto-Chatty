import socket, threading

# Global variable that mantain client's connections
connections = []
started=False


def handle_user_connection(connection: socket.socket, address: str) -> None:
    '''
        Get user connection in order to keep receiving their messages and
        sent to others users/connections.
    '''
    while True:
        try:
            # Get client message
            msg = connection.recv(1024)

            # If no message is received, there is a chance that connection has ended
            # so in this case, we need to close connection and remove it from connections list.
            if msg:
                # Log message sent by user
                print(f'{address[0]}:{address[1]} - {msg.decode()}')
                
                # Build message format and broadcast to users connected on server
                msg_to_send = f'{msg.decode()}'
                broadcast(msg_to_send, connection)

            # Close connection if no message was sent
            else:
                remove_connection(connection,connections)
                break

        except Exception as e:
            # print(f'Error to handle user connection: {e}')
            remove_connection(connection,connections
            )
            break


def broadcast(message: str, connection: socket.socket) -> None:
    '''
        Broadcast message to all users connected to the server
    '''

    # Iterate on connections in order to send message to all client's connected
    for client_conn in connections:
        # Check if isn't the connection of who's send
        if client_conn != connection:
            try:
                # Sending message to client connection
                client_conn.send(message.encode())

            # if it fails, there is a chance of socket has died
            except Exception as e:
                print('Error broadcasting message: {e}')
                remove_connection(client_conn,connections)

def remove_connection(conn: socket.socket, connections: list) -> None:
    """
    Remove specified connection from connections list and notify others
    """
    # Check if the connection is in the connections list
    
    if conn in connections:
        # Close the socket and remove the connection from the list
        conn.close()
        connections.remove(conn)  # Only remove the specified connection

        # Notify remaining connections about the disconnection
        message = "Your friend has left".encode()
        # Send the message to all other connections
        for connection in connections:
            try:
                connection.send(message)
            except socket.error:
                # Handle cases where a connection might already be closed
                pass


def server() -> None:
    global started
    '''
        Main process that receive client's connections and start a new thread
        to handle their messages
    '''

    LISTENING_PORT = 12000
    
    try:
        # Create server and specifying that it can only handle 4 connections by time!
        socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_instance.bind(('', LISTENING_PORT))
        socket_instance.listen(4)

        print('Server running!')
        
        while True:
            socket_connection, address = socket_instance.accept() 
            if(len(connections)<2):
                # Accept client connection
                connections.append(socket_connection)

                socket_connection.send(str(len(connections)).encode("utf-8"))

                # Add client connection to connections list
                # Start a new thread to handle client connection and receive it's messages
                # in order to send to others connections

                threading.Thread(target=handle_user_connection, args=[socket_connection, address]).start()
                if(len(connections)==2 and started==False):
                        connections[1].send(" start ".encode())
                        connections[0].send(" start ".encode())
                        started=True
                
                
            else:
                # If limit reached, refuse the connection
                 # Accept and then close to refuse
                socket_connection.send("Connection refused: server limit reached.".encode())
                socket_connection.close()

    except Exception as e:
        print(f'An error has occurred when instancing socket: {e}')
    finally:
        # In case of any problem we clean all connections and close the server connection
        if len(connections) > 0:
            for conn in connections:
                remove_connection(conn,connections)

        socket_instance.close()


if __name__ == "__main__":
    server()