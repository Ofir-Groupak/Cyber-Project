import socket
import threading
from DB_Handler import *
from Examinor import *
import pickle

server_ip = "127.0.0.1"
server_port =5555
client_usernames_to_objects = {}

def init_server():
    """
    Initializes a server socket, binds it to the specified IP address and port,
    and starts listening for incoming connections.

    Returns:
        socket: Initialized server socket object.
    """
    # Initialize server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen()
    print("Server is up and running!")
    return server_socket

def get_clients(server_socket):
    """
    Accepts incoming client connections, receives data from clients,
    and spawns a new thread to handle each client's requests.

    Parameters:
        server_socket (socket): Initialized server socket object.
    """
    while True:
        print("Waiting for clients!")
        client_object, client_IP = server_socket.accept()
        data = client_object.recv(1024)
        received_list = pickle.loads(data)
        print(received_list)
        client_thread = threading.Thread(target=client_handle, args=(client_object, received_list))
        client_thread.start()
def sign_up_handle(client_object,login_info):
    """
    handles the client sign up

    :param client_object:represents the client
    :param login_info:list that represents the information the client sent
    :return: None
    """
    print('info',login_info)
    add_user(login_info[1], login_info[2], login_info[3], login_info[4], login_info[5], str(login_info[6]))
    print(f"created using {login_info}")
    data = client_object.recv(1024)
    received_list = pickle.loads(data)
    client_handle(client_object,received_list)
def client_handle(client_object,login_info):
    """
    handles the client and his requests

    :param client_object: represents the client's object
    :param username: represents the username given by the user
    :return:None
    """

    if login_info[0]=="SIGNUP":
        sign_up_handle(client_object,login_info)
        return

    username = login_info[1]
    password = login_info[2]
    print(username,password)

    print(check_password(username,password))

    if check_password(username,password):

        print(f"Accepted connection from {username}")
        client_object.send("Correct".encode())
        first_symptom_handle(client_object)

    else:
        client_object.send("Try again".encode())
        login_info = client_object.recv(1024).decode().split('#')
        client_handle(client_object,login_info)

def first_symptom_handle(client_object):
    data = client_object.recv(1024).decode()
    examine(data , client_object)

def examine(first_symptom,client_object):
    """
    :param first_symptom: represents the symptom given to the user
    :param client_object: represents the client's object
    :return: None
    """
    current_symptoms = []
    current_symptoms.append(first_symptom)
    potential_diseases = list_for_symptom(first_symptom)
    potential_diseases_to_symptoms = {}

    for disease in potential_diseases:
        potential_diseases_to_symptoms[disease] = get_symptoms_for_disease(disease)

    while True:
        #print(potential_diseases_to_symptoms.keys())
        for potential_disease in potential_diseases_to_symptoms.keys():
            print(f"Currently examines for {potential_disease}")
            try:
                symptoms = potential_diseases_to_symptoms[potential_disease]
            except KeyError:
                if not potential_diseases_to_symptoms:
                    result = f"You have {potential_disease}"
                    print(result)
                    client_object.send(result.encode('utf-8'))
                    return
                break
            for potential_symptom in [x for x in symptoms if x not in current_symptoms]:
                question = (f"Do you suffer from {potential_symptom} ?").replace("_"," ")
                client_object.send(question.encode('utf-8'))
                print(f'sending {question}')
                answer =client_object.recv(1024).decode()
                #print('3')
                if answer =='no':
                    answer=False
                else:
                    answer=True

                if answer:
                    current_symptoms.append(potential_symptom)
                    potential_diseases_to_symptoms = remove_diseases_without_x(potential_diseases_to_symptoms,potential_symptom)
                    if len(potential_diseases_to_symptoms) == 1:
                        result = f"You have {list(potential_diseases_to_symptoms.keys())[0]}"
                        print(result)
                        client_object.send(result.encode('utf-8'))
                        command = client_object.recv(1024).decode()

                        if command=="Try again":
                            first_symptom_handle(client_object)
                        else:
                            return
                else:
                    #print('2')
                    potential_diseases_to_symptoms = remove_diseases_with_x(potential_diseases_to_symptoms,potential_symptom)
                    if len(potential_diseases_to_symptoms) == 1:
                        result = f"You have {list(potential_diseases_to_symptoms.keys())[0]}"
                        print(result)
                        client_object.send(result.encode('utf-8'))
                        command = client_object.recv(1024).decode()

                        if command == "Try again":
                            first_symptom_handle(client_object)
                        else:
                            return

            if len(potential_diseases_to_symptoms) == 1:
                return




if __name__=="__main__":
    server_socket = init_server()
    get_clients(server_socket)
