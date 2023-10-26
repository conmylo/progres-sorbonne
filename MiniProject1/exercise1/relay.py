import socket
import threading

# Define function to handle the client
def handle_client(client_socket, target_host, target_port):
    # Connect to the target server
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_host, target_port))

    # Relay data between the client and target server
    while True:
        # Receive data from the client
        client_data = client_socket.recv(4096)

        # Check if data contains something
        if len(client_data) == 0:
            break

        # Forward data to the target server
        target_socket.send(client_data)

        # Receive data from the target server
        target_data = target_socket.recv(4096)

        # Check if data contains something
        if len(target_data) == 0:
            break

        # Forward data back to the client
        client_socket.send(target_data)

    # Close the connections
    client_socket.close()
    target_socket.close()


# Define server relay function
def start_relay_server(server_host, server_port, target_host, target_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_host, server_port))
    server.listen(5)
    print(f"[*] Listening on {server_host}:{server_port}")

    # Server is always accepting connections
    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, target_host, target_port))
        client_handler.start()


if __name__ == "__main__":
    server_host = "0.0.0.0"  # Listen on all available network interfaces
    server_port = 1234  # Port to listen on
    target_host = "26.90.205.140"  # IP address of the target server
    target_port = 12345  # Port of the target server

    start_relay_server(server_host, server_port, target_host, target_port)
