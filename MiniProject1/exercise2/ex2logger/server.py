import socket
import threading


# Define function to handle the incoming connections
def handle_connection(client_socket, addr):
    print(f"[*] Connection from {addr[0]}:{addr[1]}")

    # Store request into variable
    request = client_socket.recv(1024).decode('utf-8')
    uri = request.split(' ')[1].encode()
    http_response = b"""\
        HTTP/1.1 200 OK

        <html>
            <head>
                <title>Server</title><
            /head>
            <body>
                <h1>This is a response from the TCP server!</h1>
            </body>
        </html>
        """
    client_socket.send(http_response)
    client_socket.close()

# Define function to start server
def start_tcp_server():
    HOST = '0.0.0.0'  # Listen on all available interfaces
    PORT = 12345

    # Initialize server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] TCP Server Listening on {HOST}:{PORT}")

    # Server is always accepting new connections
    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_connection, args=(client_socket, addr))
        client_handler.start()

# In main start the server
if __name__ == "__main__":
    start_tcp_server()
