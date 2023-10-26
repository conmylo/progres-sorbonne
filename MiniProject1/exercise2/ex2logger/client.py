import socket


# Define function to emulate a client
def start_tcp_client():
    HOST = '127.0.0.1'
    PORT = 1234

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    req = input("Enter the type of request (e.g. GET or POST): ")
    uri = input("Enter URI (e.g. /resource1): ")  # Get URI from user
    request = f"{req} {uri} HTTP/1.1\r\nHost: localhost\r\n\r\n"
    client.sendall(request.encode())

    response = client.recv(4096)
    print(f"Received: {response.decode('utf-8')}")

    client.close()


# In main start the client emulation
if __name__ == "__main__":
    start_tcp_client()
