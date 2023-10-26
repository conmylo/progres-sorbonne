import socket
import threading
import os

# Name the cache directory
CACHE_DIR = 'cache'

# Create the cache directory if it does not exist
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


# Define function to handle the client
def handle_client(client_socket, target_host, target_port):
    request = client_socket.recv(4096).decode('utf-8')
    method, uri, _ = request.split(' ', 2)

    # Re-format the cache path
    cache_path = os.path.join(CACHE_DIR, uri.replace('/', '_'))

    # If the content exists in cache and it is GET request, serve it and close socket
    if method == "GET" and os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            client_socket.sendall(f.read())
        client_socket.close()
        return

    # Otherwise create a socket and fetch the content from the server
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_host, target_port))
    target_socket.sendall(request.encode())

    # Store the response into a variable to use later
    response = target_socket.recv(4096)

    # Save response to cache
    if method == "GET":
        with open(cache_path, 'wb') as f:
            f.write(response)
            f.write(b'cached response')

    # Send response to client
    client_socket.sendall(response)

    # Close the socket
    client_socket.close()
    target_socket.close()


# Define function to initialize relay server
def start_relay_server(server_host, server_port, target_host, target_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_host, server_port))
    server.listen(5)
    print(f"[*] Listening on {server_host}:{server_port}")

    # Server always accepts connections
    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, target_host, target_port))
        client_handler.start()


# In main define the IP Addresses and ports and start the server - relay connection
if __name__ == "__main__":
    server_host = "0.0.0.0"
    server_port = 1234
    target_host = "127.0.0.1"
    target_port = 12345

    start_relay_server(server_host, server_port, target_host, target_port)
