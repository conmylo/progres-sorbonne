import socket
import time

# Define the server port and IP address
serverPort = 1234
serverIp= '26.90.205.140'
ADDR = (serverIp, serverPort)

# Create the socket and connect to the address
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(ADDR)

# Ask for input
message = input('sentence:').encode('utf-8')

# Send the message
clientSocket.send(message)

# Receive and print the modified message
modifiedMessage = clientSocket.recv(2048)
print(modifiedMessage)

# Close the socket
clientSocket.close()
