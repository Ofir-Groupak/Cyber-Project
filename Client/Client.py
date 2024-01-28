import socket
from GUI import *

def start_client():
    server_ip = '127.0.0.1'
    server_port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    return client_socket
def client_start_socket(client):
    global END

    data_receive = client_socket.recv(1024).decode()
    send_data = input(f"{data_receive}")
    client.send(send_data.encode('utf-8'))

    while True:

        data_receive = client.recv(1024).decode()
        send_data = input(f"{data_receive}")
        client.send(send_data.encode('utf-8'))


if __name__ == "__main__":
    client_socket = start_client()
    client_socket.send(input("Enter Username:").encode())

    client_start_socket(client_socket)
