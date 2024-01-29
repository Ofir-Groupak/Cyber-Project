import socket
import threading
from DB_Handler import *
from Examinor import *

server_ip = "172.20.135.88"
server_port =5555
client_usernames_to_objects = {}

def init_server():
    # Initialize server socket
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((server_ip,server_port))
    server_socket.listen()
    print("Server is up and running!")
    return server_socket

def get_clients(server_socket):
    # Accept incoming client connections

    while True:
        print("Waiting for clients!")
        client_object ,client_IP =  server_socket.accept()
        data = client_object.recv(1024).decode().split('#')
        username = data[0]
        client_thread = threading.Thread(target=client_handle, args=(client_object,username))
        client_thread.start()


def client_handle(client_object,username):
    """
    :param client_object: represents the client's object
    :param username: represents the username given by the user
    :return:None
    """
    print(f"Accepted connection from {username}")
    client_object.send(f"Hello {username}!, Enter your first symptom: ".encode())
    data = client_object.recv(1024).decode()
    examine_thread = threading.Thread(target=examine, args=(data,client_object))
    examine_thread.start()

    #examine(data,client_object)


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
                question = (f"do you suffer from {potential_symptom} ? answer yes/no")
                client_object.send(question.encode('utf-8'))
                #print('2')
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
                        return
                else:
                    #print('2')
                    potential_diseases_to_symptoms = remove_diseases_with_x(potential_diseases_to_symptoms,potential_symptom)
                    if len(potential_diseases_to_symptoms) == 1:
                        result = f"You have {list(potential_diseases_to_symptoms.keys())[0]}"
                        print(result)
                        client_object.send(result.encode('utf-8'))
                        return

            if len(potential_diseases_to_symptoms) == 1:
                return




if __name__=="__main__":
    server_socket = init_server()
    get_clients(server_socket)





