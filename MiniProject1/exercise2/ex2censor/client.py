import socket


# Define function to emulate a client
def start_tcp_client():
    # Define IP address and port
    HOST = '127.0.0.1'
    PORT = 12340

    # Create a socket for the client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Require user input
    req = input("Enter the type of request (e.g. GET or POST): ")
    uri = input("Enter URI (e.g. /resource1): ")

    # Format the request
    request = f"{req} {uri} HTTP/1.1\r\nHost: localhost\r\n\r\n"
    client.sendall(request.encode())

    # Store response into variable
    response = client.recv(4096)
    print(f"Received: {response.decode('utf-8')}")

    # Close the client's socket
    client.close()


# In main start the client emulation
if __name__ == "__main__":
    start_tcp_client()
