import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

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
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, message + '\n')  # Display the message
            chat_box.yview(tk.END)  # Scroll to the bottom
            chat_box.config(state=tk.DISABLED)
        except:
            print("An error occurred.")
            client.close()
            break

# Function to send messages
def send_message():
    message = message_entry.get()  # Get message from the input field
    if message:
        client.send(message.encode())  # Send message to server
        message_entry.delete(0, tk.END)  # Clear input field

# Request nickname
def request_nickname():
    nickname = nickname_entry.get()
    if nickname:
        client.send(nickname.encode())  # Send nickname to server
        nickname_window.destroy()  # Close the nickname window
        # Start receiving and sending threads
        threading.Thread(target=receive_messages, daemon=True).start()

# Create the main chat window
root = tk.Tk()
root.title("Chat Client")

# Create a separate window for entering the nickname
nickname_window = tk.Toplevel(root)
nickname_window.title("Enter Nickname")
nickname_label = tk.Label(nickname_window, text="Enter your nickname:")
nickname_label.pack(padx=10, pady=5)
nickname_entry = tk.Entry(nickname_window)
nickname_entry.pack(padx=10, pady=5)
nickname_button = tk.Button(nickname_window, text="Submit", command=request_nickname)
nickname_button.pack(padx=10, pady=5)

# Create a text area for displaying the chat messages
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
chat_box.pack(padx=10, pady=10)

# Create a message entry field and send button
message_entry = tk.Entry(root, width=40)
message_entry.pack(side=tk.LEFT, padx=10, pady=5)
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=10, pady=5)

# Run the GUI
root.mainloop()
