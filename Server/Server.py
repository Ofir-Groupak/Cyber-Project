import socket
import threading
from DB_Handler import *

server_ip = "127.0.0.1"
server_port =5555
client_usernames_to_objects = {}

def init_server():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((server_ip,server_port))
    server_socket.listen()
    print("Server is up and running!")
    return server_socket

def get_clients(server_socket):
    print("Waiting for clients!")
    client_object ,client_IP =  server_socket.accept()
    data = client_object.recv(1024).decode().split('#')
    username = data[0]
    password = data[1]
    if(check_password(username,password)):
        client_usernames_to_objects[username] = client_object
        client_thread = threading.Thread(target=client_handle, args=(client_object, username))
        client_thread.start()
    else:
        print("wrong password")

def client_handle(client_object,username):
    print(f"Accepted connection from {username}")
    client_object.send("Login Accepted".encode())
    while True:
        data = client_object.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')
        print(f"Received from {username}: {message}")

        response = f"Server received: {message}"
        client_object.send(response.encode('utf-8'))

    print(f"Connection from {username} closed.")
    client_object.close()

if __name__=="__main__":
    server_socket = init_server()
    get_clients(server_socket)





