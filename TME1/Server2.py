import socket
import time

SERVER_PORT = 12345

def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', SERVER_PORT))
    print(f"Time server is listening on port {SERVER_PORT}")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        if data.decode('utf-8') == 'get_time':
            current_time = time.ctime()
            server_socket.sendto(current_time.encode('utf-8'), client_address)

if __name__ == '__main__':
    run()
