import socket
import threading

# Server Configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

# Create a socket (IPv4, TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []  # List of connected clients
nicknames = {}  # Store client nicknames

# Function to broadcast messages to all clients
def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            client.send(message)

# Function to handle individual client connections
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)  # Receive message
            if not message:
                break
            broadcast(message, sender=client)  # Send message to others
        except:
            clients.remove(client)
            client.close()
            break

# Function to accept new client connections
def receive_connections():
    print(f"Server is listening on {HOST}:{PORT}...")
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")
        
        # Request and store nickname
        client.send("NICKNAME".encode())
        nickname = client.recv(1024).decode()
        nicknames[client] = nickname
        clients.append(client)

        print(f"Nickname of new client: {nickname}")
        broadcast(f"{nickname} has joined the chat!".encode())

        # Start a thread for this client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive_connections()
