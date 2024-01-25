import pandas as pd

df = pd.read_csv(r'dataset1.csv').drop_duplicates(subset=['Disease'])

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

    updated_diseases = {}
    for disease in diseases.keys():
        if ' '+symptom in diseases[disease]:
            print(f"Removing {disease} due to {symptom}")
            continue
        updated_diseases[disease] = get_symptoms_for_disease(disease)

    return updated_diseases

def remove_diseases_without_x(diseases,symptom):

    updated_diseases = {}
    for disease in diseases.keys():
        if ' '+symptom in diseases[disease]:
            updated_diseases[disease] = get_symptoms_for_disease(disease)
        else:
            print(f"Removing {disease} due to not having {symptom}")

    return updated_diseases




if __name__=="__main__":

    current_symptoms = []
    first_symptom = "fever"
    #first_symptom = input("Enter your most severe symptom : ")
    current_symptoms.append(first_symptom)
    potential_diseases = list_for_symptom(first_symptom)
    potential_diseases_to_symptoms = {}

    for disease in potential_diseases:
        potential_diseases_to_symptoms[disease] = get_symptoms_for_disease(disease)

    print(remove_diseases_without_x(potential_diseases_to_symptoms,'high_fever'))


















