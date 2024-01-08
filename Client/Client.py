import socket


def start_client():
    server_ip = '127.0.0.1'
    server_port = 5555

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    message = input("Enter Username:")
    client_socket.send(message.encode('utf-8'))

    while True:
        message = input("Enter a message to send to the server (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        client_socket.send(message.encode('utf-8'))

        # Receive and print the server's response
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")

    client_socket.close()


if __name__ == "__main__":
    start_client()