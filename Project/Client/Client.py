import socket
from RegularUser import *

def start_client():
    #starts client
    server_ip = '172.20.137.60'
    server_port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    return client_socket


if __name__ == "__main__":
    client_socket = start_client()
    LoginPageGUI(client_socket)
