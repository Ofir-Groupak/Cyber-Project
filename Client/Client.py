
import socket

PORT = 6060
SERVER = "127.0.0.1"
END = True
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect((SERVER,PORT))

def client_socket(send_data):
    global END
    #send_data = input("Input your Username :")
    client.send(send_data.encode())
    if send_data.lower() == "bye":
        client.close()
        END = False
    else:
        data_receive = client.recv(1024).decode()
        print(f"{data_receive}")

client_socket(input("Input your Username :"))
while END:
    client_socket(input("Input your message :"))