import socket
import threading
from Project.Server.Diseases_db_handler import *
import pickle
from DB_Handler import *
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

server_ip = "127.0.0.1"
server_port = 4444
client_usernames_to_objects = {}
object_to_keys = {}


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

    global server_private_key, server_public_key
    server_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    server_public_key = server_private_key.public_key()

    return server_socket
def decrypt_with_private_key(data):
    return server_private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def encrypt_with_public_key(data, client_object):
    print(object_to_keys, type(object_to_keys[client_object]))
    return object_to_keys[client_object].encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


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

        client_object.send(server_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
        client_public_key_pem = client_object.recv(2048)
        client_public_key = serialization.load_pem_public_key(
            client_public_key_pem,
            backend=default_backend()
        )
        global object_to_keys
        object_to_keys[client_object] = client_public_key
        client_thread = threading.Thread(target=client_handle, args=(client_object,))
        client_thread.start()


def sign_up_handle(client_object):
    """
    handles the client sign up

    :param client_object:represents the client
    :param login_info:list that represents the information the client sent
    :return: None
    """
    print("in sign up handle")
    print(get_all_doctors())
    options = [get_all_diseases(), get_all_doctors(), None]
    client_object.send(encrypt_with_public_key(pickle.dumps(options), client_object))

    login_info = client_object.recv(1024)
    login_info = decrypt_with_private_key(login_info)
    login_info = pickle.loads(login_info)
    print(login_info)

    if "LOGIN" == login_info[0]:
        client_handle(client_object)

    add_user(login_info[1], login_info[2], login_info[3], login_info[4], login_info[5], str(login_info[6]),
             str(login_info[7]))
    print(f"created using {login_info}")
    client_object.send(encrypt_with_public_key("sucsess".encode(),client_object))

    client_handle(client_object)


def client_handle(client_object):
    """
    handles the client and his requests

    :param client_object: represents the client's object
    :return:None
    """
    print("in client handle")

    login_info = client_object.recv(1024)
    print(login_info)
    login_info = decrypt_with_private_key(login_info)
    login_info = pickle.loads(login_info)
    print(login_info)

    if login_info[0] == "SIGNUP":
        sign_up_handle(client_object)
        return

    username = login_info[1]
    password = login_info[2]
    print(username, password)

    print(check_password(username, password))

    if check_password(username, password):

        print(f"Accepted connection from {username}")
        response = ["Correct", is_doctor(username)]
        client_object.send(pickle.dumps(response))

        if is_doctor(username) == "False":
            print("menu")
            menu_handle(client_object, username)
        else:
            menu_handle(client_object, username)
    else:
        client_object.send(pickle.dumps("Try again".encode()))
        client_handle(client_object)


def menu_handle(client_object, username):
    print("in menu handle")

    custom_menu = str(is_doctor(username))
    data = encrypt_with_public_key(custom_menu.encode(),client_object)
    client_object.send(data)

    data = client_object.recv(1024)
    data = decrypt_with_private_key(data).decode()
    print(data)
    if "examine" in data:
        first_symptom_handle(client_object, username)
    if "open messages" in data:
        data = encrypt_with_public_key(pickle.dumps(get_all_messages_for_user(username)), client_object)
        client_object.send(data)
        view_messages_handle(client_object, username)
    if "send message" in data:
        send_message_handle(client_object, username)
    if "logout" in data:
        client_handle(client_object)


def send_message_handle(client_object, username):
    print("in send message handle")

    options = []
    if is_doctor(username) == "False":
        options.append(get_doctor_for_user(username))

    else:
        options = get_all_patients(username)

    options = encrypt_with_public_key(pickle.dumps(options), client_object)
    client_object.send(options)

    data = client_object.recv(1024)
    data = decrypt_with_private_key(data)
    data = pickle.loads(data)

    while "menu" != data[0]:

        try:
            print(data)
            add_message(username, data[1], data[2], data[3])
            data = client_object.recv(1024)
            data = decrypt_with_private_key(data)
            data = pickle.loads(data)
        except IndexError:
            break

    if is_doctor(username):
        data = encrypt_with_public_key("DOCTOR".encode(), client_object)
        client_object.send(data)
        menu_handle(client_object, username)

    else:
        data = encrypt_with_public_key("MENU".encode(), client_object)
        client_object.send(data)
        menu_handle(client_object, username)


def view_messages_handle(client_object, username):
    print("in view messages handle")

    data = client_object.recv(1024)
    print(data)
    data = decrypt_with_private_key(data)
    data = pickle.loads(data)
    print(data)
    if "menu" in data[0]:
        if is_doctor(username):
            data = encrypt_with_public_key("DOCTOR".encode(), client_object)
            client_object.send(data)
            menu_handle(client_object, username)

        else:
            data = encrypt_with_public_key("MENU".encode(), client_object)
            client_object.send(data)
            menu_handle(client_object, username)

    if "reply" in data[0]:
        send_message_handle(client_object, username)


def first_symptom_handle(client_object, username):
    print("in first symptom handle")
    data = encrypt_with_public_key(pickle.dumps(get_all_symptoms()), client_object)
    client_object.send(data)
    data = client_object.recv(1024)
    data = decrypt_with_private_key(data).decode()
    examine(data, client_object, username)


def information_page_handle(client_object, result, username):
    print("in information page handle")
    data = encrypt_with_public_key(pickle.dumps(get_advice_for_disease(result)), client_object)
    client_object.send(data)
    data = client_object.recv(1024)
    data = decrypt_with_private_key(data)
    menu_handle(client_object, username)


def examine(first_symptom, client_object, username):
    print("in examine")

    user_symptoms = []
    user_symptoms.append(first_symptom)
    asked_symptoms = [first_symptom]
    potential_diseases = get_history_of_diseases(username)
    potential_diseases.extend(get_diseases_with_symptom(first_symptom))
    possible_scenarios = []
    for potential_disease in list(dict.fromkeys(potential_diseases)):
        possible_scenarios.extend(possible_scenarios_for_disease(potential_disease))
    possible_scenarios = remove_scenarios_without_x(possible_scenarios, first_symptom)

    result = ""
    print(f"Potential Diseases : {list(dict.fromkeys(potential_diseases))}")
    lst = []
    while result == "":
        for scenario in possible_scenarios:

            print(f"possible scenarios : {len(possible_scenarios)} \n current scenario :{scenario}")
            print(get_diseases_by_scenarios(possible_scenarios))

            potential_symptom = get_next_symptom(scenario, asked_symptoms)
            if (potential_symptom == "" and get_diseases_by_scenarios(possible_scenarios)):
                print(f"moving to next scenario : {possible_scenarios}")
                continue

            asked_symptoms.append(potential_symptom)
            question = f"Do you suffer from{potential_symptom}?".replace("_", " ")

            data = encrypt_with_public_key(question.encode(), client_object)
            client_object.send(data)

            answer = client_object.recv(1024)
            answer = decrypt_with_private_key(answer).decode()


            if answer == "yes":
                print('aaaaaaa',user_symptoms)
                possible_scenarios = remove_scenarios_without_x(possible_scenarios, potential_symptom)
                user_symptoms.append(potential_symptom)

            else:
                possible_scenarios = remove_scenarios_with_x(possible_scenarios, potential_symptom)

            if len((get_diseases_by_scenarios(possible_scenarios))) == 1:
                result = get_disease_by_symptoms(possible_scenarios[0])
            break

    disease = result
    result = f"You have {disease}"
    result = encrypt_with_public_key(result.encode(), client_object)
    client_object.send(result)

    action = client_object.recv(1024)
    action = decrypt_with_private_key(action)
    action = pickle.loads(action)
    add_disease(username, disease)
    print(action)
    if action[1] == "yes":
        user_symptoms = ','.join(user_symptoms)
        add_message(username, get_doctor_for_user(username), f"{username} Diagnosis",
                    f"Symptoms : {user_symptoms},\nResult : {disease}")

    if action[0] == "Information":
        information_page_handle(client_object, disease, username)
    else:
        menu_handle(client_object, username)


if __name__ == "__main__":
    server_socket = init_server()
    get_clients(server_socket)

    # print(get_all_diseases())
    # print(get_symptoms_for_disease('Malaria'))

    # examine('itching',None,None)
    # print(get_diseases_with_symptom('acidity'))
    # #print(possible_scenarios_for_disease('Common Cold'))
