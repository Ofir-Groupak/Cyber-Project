def examine(first_symptom,client_object, username):
    """
    :param first_symptom: represents the symptom given to the user
    :param client_object: represents the client's object
    :return: None
    """
    print("in examine")
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

                    command = client_object.recv(1024)
                    action = pickle.loads(command)
                    add_disease(username, disease)

                    if action[1] == "yes":
                        final_symptoms = ""
                        for symptom in current_symptoms:
                            final_symptoms += (str(symptom)[1:len(symptom)]) + ", "
                        print("sending!!!!!!!")
                        add_message(username, get_doctor_for_user(username), f"{username} Diagnosis",
                                    f"Symptoms : {final_symptoms},\nResult : {disease}")
                    if action[0] == "Information":
                        information_page_handle(client_object, disease, username)
                    else:
                        menu_handle(client_object, username)
                break
            for potential_symptom in [x for x in symptoms if x not in current_symptoms]:
                question = (f"Do you suffer from{potential_symptom} ?").replace("_"," ")
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
                        disease = list(potential_diseases_to_symptoms.keys())[0]
                        result = f"You have {disease}"

                        print(result)
                        client_object.send(result.encode('utf-8'))
                        command = client_object.recv(1024)
                        action = pickle.loads(command)
                        add_disease(username, disease)

                        if action[1]=="yes":
                            final_symptoms =""
                            for symptom in current_symptoms:
                                final_symptoms+=(str(symptom)[1:len(symptom)]) +", "
                            print("sending!!!!!!!")
                            add_message(username, get_doctor_for_user(username),f"{username} Diagnosis",f"Symptoms : {final_symptoms},\nResult : {disease}")
                        if action[0]=="Information":
                            information_page_handle(client_object,disease,username)
                        else:
                            menu_handle(client_object,username)

                else:
                    potential_diseases_to_symptoms = remove_diseases_with_x(potential_diseases_to_symptoms,potential_symptom)
                    if len(potential_diseases_to_symptoms) == 1:
                        disease = list(potential_diseases_to_symptoms.keys())[0]
                        result = f"You have {disease}"

                        print(result)
                        client_object.send(result.encode('utf-8'))
                        command = client_object.recv(1024)
                        action = pickle.loads(command)
                        add_disease(username, disease)

                        if action[1] == "yes":
                            final_symptoms = ""
                            for symptom in current_symptoms:
                                final_symptoms += (str(symptom)[1:len(symptom)]) + ", "
                            print("sending!!!!!!!")
                            add_message(username, get_doctor_for_user(username),f"{username} Diagnosis",f"Symptoms : {final_symptoms},\nResult : {disease}")
                        if action[0] == "Information":
                            information_page_handle(client_object,disease,username)
                        else:
                            menu_handle(client_object, username)

            if len(potential_diseases_to_symptoms) == 1:
                disease = list(potential_diseases_to_symptoms.keys())[0]
                result = f"You have {disease}"

                print(result)
                client_object.send(result.encode('utf-8'))
                command = client_object.recv(1024)
                action = pickle.loads(command)
                add_disease(username, disease)

                if action[1] == "yes":
                    final_symptoms = ""
                    for symptom in current_symptoms:
                        final_symptoms += (str(symptom)[1:len(symptom)]) + ", "
                    print("sending!!!!!!!")
                    add_message(username, get_doctor_for_user(username),f"{username} Diagnosis",f"Symptoms : {final_symptoms},\nResult : {disease}")
                if action[0] == "Information":
                    information_page_handle(client_object, disease, username)
                else:
                    menu_handle(client_object, username)

