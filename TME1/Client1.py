import socket
import time

# Server configuration
SERVER_HOST = '172.20.10.1'  # Replace with the actual IP address or hostname of the server
SERVER_PORT = 12345

# Number of PING requests
NUM_REQUESTS = 10

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Store the start time
start_time = time.time()

# Send PING requests and measure RTT
for i in range(NUM_REQUESTS):
    message = f"PING {i}"
    client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))

    # Set a timeout for the response
    client_socket.settimeout(1)

    try:
        data, server_address = client_socket.recvfrom(1024)
        end_time = time.time()
        rtt = (end_time - start_time) * 1000  # Calculate RTT in milliseconds
        print(f"Received from {server_address}: {data.decode()}, RTT = {rtt:.2f} ms")
    except socket.timeout:
        print("Request timed out")

    # Reset the start time for the next request
    start_time = time.time()

client_socket.close()
