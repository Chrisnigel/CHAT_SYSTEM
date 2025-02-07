import socket
import threading

# Server Configuration
HOST = '127.0.0.1'  # Server IP
PORT = 12345        # Port to connect to

# Create a socket (IPv4, TCP)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Function to handle receiving messages
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()  # Receive message from server
            print(message)  # Display the message
        except:
            print("An error occurred.")
            client.close()
            break

# Function to send messages
def send_messages():
    while True:
        message = input()  # Get user input
        client.send(message.encode())  # Send message to server

# Request nickname
nickname = input("Enter your nickname: ")
client.send(nickname.encode())  # Send nickname to server

# Start receiving and sending threads
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()