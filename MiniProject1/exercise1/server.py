import socket

# Define the server IP and port
serverIp = socket.gethostbyname(socket.gethostname())
print(serverIp)
server_port = 12345

# Create a socket and bind it to the address
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverIp, server_port))
print(f"Server listening on {serverIp}:{server_port}")
serverSocket.listen(1)

# Server socket is always accepting connections
while True:
    clientSocket, client_address = serverSocket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # Receive message from client
    message = clientSocket.recv(2048)

    # Modify the message to uppercase
    modifiedMessage = message.upper()

    # Send back the modified message
    clientSocket.send(modifiedMessage)

    # Close the socket
    clientSocket.close()
