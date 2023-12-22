import socket
import random

# Server configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the server address
server_socket.bind((HOST, PORT))

print(f"Server is listening on {HOST}:{PORT}")

while True:
    data, client_address = server_socket.recvfrom(1024)

    # Simulate a 50% chance of not responding to requests
    if random.random() < 0.5:
        print(f"Server did not respond to a request from {client_address}")
        continue

    # Echo the received data back to the client
    server_socket.sendto(data, client_address)
    print(f"Server sent a response to {client_address}")
