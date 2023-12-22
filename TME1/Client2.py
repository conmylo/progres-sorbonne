import socket
import time

SERVER_IP = '172.20.10.1'
SERVER_PORT = 12345


def get_time_difference():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto('get_time'.encode('utf-8'), (SERVER_IP, SERVER_PORT))

    server_time = client_socket.recv(1024).decode('utf-8')
    client_time = time.ctime()

    print(f"Server Time: {server_time}")
    print(f"Client Time: {client_time}")

    server_time_struct = time.strptime(server_time)
    client_time_struct = time.strptime(client_time)

    server_timestamp = time.mktime(server_time_struct)
    client_timestamp = time.mktime(client_time_struct)

    time_difference = server_timestamp - client_timestamp
    return time_difference


if __name__ == '__main__':
    time_difference = get_time_difference()
    print(f"Time Difference (Server - Client): {time_difference} seconds")
