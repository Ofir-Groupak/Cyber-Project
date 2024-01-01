import socket
import threading

SERVER_IP = "127.0.0.1"
SERVER_PORT =6060
clients_usernames = []
clients_objects = []

def init_server():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP,SERVER_PORT))
    server_socket.listen()
    print(" waiting for clients")
    return server_socket

def client_session(client_object,username):
    while True:
        data = client_object.recv(1024).decode()
        if data.lower() == "bye":
            print(f" {username} is disconnected")
            client_object.close()
            break
        print(username+" :",data )
        client_object.send("Ack".encode())



def main():
    server_socket = init_server()
    while True:
        client_object ,client_IP =  server_socket.accept()
        print(client_object)
        print(client_IP)
        clients_objects.append(client_object)
        username = client_object.recv(1024).decode()
        clients_usernames.append(username)
        client_object.send("Welcome to Server".encode())
        client_th = threading.Thread(target=client_session, args=(client_object,username))
        client_th.start()


main()