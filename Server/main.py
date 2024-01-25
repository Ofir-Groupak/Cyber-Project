import pandas as pd

df = pd.read_csv(r'C:\Users\student\PycharmProjects\Cyber-Project1\Server\dataset1.csv').drop_duplicates(subset=['Disease'])

def list_for_symptom(symptom):
    lst = []
    for disease in df.itertuples():
        for i in range(2,17):
            try:
                if disease[i].find(symptom) != -1:
                    lst.append(disease[1])
            except AttributeError:
                continue
    return lst

def get_index_for_disease(illness):
    for disease in df.itertuples():
        if disease[1] == illness:
            return disease[0]
    return -1
def get_symptoms_for_disease(disease):
    symptoms = []
    #all_symptoms = df.iloc[get_index_for_disease(disease)]
    for symptom in [x for x in df.itertuples() if x[1]==disease]:
        for i in range(2,17):
            symptoms.append(symptom[i])

    return [x for x in symptoms if not pd.isna(x)]

def remove_diseases_with_x(diseases,symptom):

    for disease in diseases:
        #print(' '+symptom,get_symptoms_for_disease(disease))
        #print(get_symptoms_for_disease(disease[0]).__contains__(symptom))
        if symptom in get_symptoms_for_disease(disease[0]):
            #print(f"Removing {disease} because of {symptom}")
            diseases.remove(disease)
    return diseases



if __name__=="__main__":
    answer = True

    current_symptoms = []
    first_symptom = "fever"
    #first_symptom = input("Enter your most severe symptom : ")
    current_symptoms.append(first_symptom)
    potential_diseases = list_for_symptom(first_symptom)

    while len(potential_diseases) >= 2:
        disease_and_symptoms = []
        for illness in potential_diseases:
            disease_and_symptoms.append([illness, get_symptoms_for_disease(illness)])


        while answer:
            if len(potential_diseases) >=2:

                for potential_disease in disease_and_symptoms:
                    answer = True
                    for potential_symptom in potential_disease[1]:
                        answer = input(f"do you have {potential_symptom} ?")
                        if answer=='no':
                            answer=False

                        if not answer:
                            disease_and_symptoms = remove_diseases_with_x(disease_and_symptoms,potential_symptom)
                            print(disease_and_symptoms)
                            break

            else:
                print(f"You have {potential_disease}")

        print("OUT")

















