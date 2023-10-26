import socket
import threading
import os
import time

# Name the log file
LOG_FILE = 'http_log.txt'

# Define function to write the responses/requests in the log file
def write_log(message):
    with open(LOG_FILE, 'a') as f:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        f.write(f"[{timestamp}] {message}\n")


# Define function to handle the client
def handle_client(client_socket, target_host, target_port):
    # Store the request, the request type and the uri into variables
    request = client_socket.recv(4096).decode('utf-8')
    method, uri, _ = request.split(' ', 2)

    # Check the request method
    if method == "GET":
        write_log(f"{client_socket.getpeername()[0]} GET {uri}")

    # Forward request to target server
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_host, target_port))
    target_socket.sendall(request.encode())

    # Check that response is not empty and the method is "GET"
    response = target_socket.recv(4096)
    if len(response) > 0 and method == "GET":
        write_log(f"Server Response for {uri} Size: {len(response)}")

    # Send response back to the client
    client_socket.sendall(response)

    # Close the sockets
    client_socket.close()
    target_socket.close()


# Define function to initialize the relay
def start_relay_server(server_host, server_port, target_host, target_port):
    # Initialize the socket and bind it to a connection
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_host, server_port))
    server.listen(5)
    print(f"[*] Listening on {server_host}:{server_port}")

    # Always accept new connections
    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, target_host, target_port))
        client_handler.start()


# In main declare the IP addresses and the ports
if __name__ == "__main__":
    server_host = "0.0.0.0"
    server_port = 1234
    target_host = "127.0.0.1"
    target_port = 12345

    start_relay_server(server_host, server_port, target_host, target_port)
