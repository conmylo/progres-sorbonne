import socket
import os

# Server configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 8080  # Use a port number other than 80 if needed


# Function to handle HTTP requests
def handle_request(request):
    # Extract the requested filename from the request
    try:
        filename = request.split()[1]
        filename = filename.lstrip('/')

        # If the filename is empty, set it to 'index.html'
        if filename == '':
            filename = 'index.html'

        # Check if the file exists in the server's file system
        if os.path.isfile(filename):
            with open(filename, 'rb') as file:
                content = file.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n".encode('utf-8') + content
        else:
            # File not found (404 error)
            response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found.".encode('utf-8')
    except Exception as e:
        # Server error (500 error)
        response = "HTTP/1.1 500 Internal Server Error\r\n\r\nInternal Server Error.".encode('utf-8')
        print(str(e))

    return response


# Create a TCP socket and bind it to the server address
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)
print(f"Server is listening on {HOST}:{PORT}")

while True:
    # Accept incoming connection
    client_socket, client_address = server_socket.accept()

    # Receive the client's HTTP request
    request = client_socket.recv(1024).decode('utf-8')

    # Handle the request and generate a response
    response = handle_request(request)

    # Send the response to the client
    client_socket.send(response)

    # Close the connection
    client_socket.close()
