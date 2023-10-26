import socket
import threading


# Define function to store a bad message in a response
def badMessage():
    response = b"""HTTP/1.0 404 ERROR
    Server: Python/3.8.10
    Date: Now
    Content-Type: text/html
    Content-length: 127

    <!DOCTYPE>
    <html>
        <head>
            <title>Error</title>
        </head>
        <body>
            <h1>FORBIDDEN</h1>
        </body>
    </html>"""
    return response


# Define function to handle client
def handle_client(client_socket, target_host, target_port, censored_uri):
    request = client_socket.recv(4096).decode('utf-8')
    method, uri, _ = request.split(' ', 2)
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Store the response into a variable to use later depending on censored uri
    if method == "GET" and uri in censored_uri:
        response = badMessage()
    else:
        # Otherwise create a socket and fetch the content from the server
        target_socket.connect((target_host, target_port))
        target_socket.sendall(request.encode())
        response = target_socket.recv(4096)



    # Send response to client
    client_socket.sendall(response)

    # Close the socket
    client_socket.close()
    target_socket.close()


# Define function to start the relay server
def start_relay_server(server_host, server_port, target_host, target_port, censored_uri):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_host, server_port))
    server.listen(5)
    print(f"[*] Listening on {server_host}:{server_port}")

    # Serve always accepting new connections
    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, target_host, target_port,censored_uri ))
        client_handler.start()

# In main define the IP addresses and ports, as well as the forbidden uris
if __name__ == "__main__":
    server_host = "0.0.0.0"
    server_port = 12340
    target_host = "127.0.0.1"
    target_port = 12341
    CENSORED_URI = {'/bad', '/wrong', '/no'}

    start_relay_server(server_host, server_port, target_host, target_port, CENSORED_URI)
