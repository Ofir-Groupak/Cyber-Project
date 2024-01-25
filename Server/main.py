import pandas as pd

df = pd.read_csv(r'C:\Users\Ofir\PycharmProjects\Cyber-Project\Diseases Databases\dataset.csv').drop_duplicates(subset=['Disease'])

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
    all_symptoms = df.iloc[get_index_for_disease(disease)]
    for number in range(1,17):
        symptoms.append((all_symptoms[number]))
    return [x for x in symptoms if not pd.isna(x)]

def remove_diseases_with_x(diseases,symptom):
    for disease in diseases:
        print(disease)
        if ' '+symptom in get_symptoms_for_disease(disease):
            diseases.remove(disease)
    return diseases



if __name__=="__main__":


    current_symptoms = []
    first_symptom = input("Enter your most severe symptom : ")
    current_symptoms.append(first_symptom)
    potential_diseases = list_for_symptom(first_symptom)

    print(potential_diseases)












