import pandas as pd

df = pd.read_csv(r'C:\Users\Ofir\PycharmProjects\Cyber-Project2\Project\Server\DiseasesDatabases\dataset.csv').drop_duplicates(subset=['Disease'])

def list_for_symptom(symptom):
    """
    :param symptom:represents a string to a symptom
    :return:list of that symptom
    """
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
    """
    :param illness:string represents disease
    :return:the index of that disease
    """
    for disease in df.itertuples():
        if disease[1] == illness:
            return disease[0]
    return -1
def get_symptoms_for_disease(disease):
    """

    :param disease: represents a string with disease
    :return: all the symptoms for that disease
    """
    symptoms = []
    #all_symptoms = df.iloc[get_index_for_disease(disease)]
    for symptom in [x for x in df.itertuples() if x[1]==disease]:
        for i in range(2,17):
            symptoms.append(symptom[i])

    return [x for x in symptoms if not pd.isna(x)]

def remove_diseases_with_x(diseases,symptom):
    """
    :param diseases: represents a dictionary with diseases and their symptoms
    :param symptom:represents a given stirng with symptom
    :return: a dictionary without diseases with certain symptom
    """
    updated_diseases = {}
    for disease in diseases.keys():
        if symptom in diseases[disease]:
            print(f"Removing {disease} due to {symptom}")
            continue
        updated_diseases[disease] = get_symptoms_for_disease(disease)

    return updated_diseases

def remove_diseases_without_x(diseases,symptom):
    """
    :param diseases: represents a dictionary with diseases and their symptoms
    :param symptom:represents a given stirng with symptom
    :return: a dictionary with diseases with certain symptom
    """
    updated_diseases = {}
    for disease in diseases.keys():
        if symptom in diseases[disease]:
            updated_diseases[disease] = get_symptoms_for_disease(disease)
        else:
            print(f"Removing {disease} due to not having {symptom}")

    return updated_diseases

def get_all_symptoms():
    """
    :return: all the symptoms
    """
    return list(dict.fromkeys(df['Symptom_1'].tolist()))

def get_all_diseases():
    """
    :return:all the diseases
    """
    return list(dict.fromkeys(df['Disease'].tolist()))

def get_advice_for_disease(disease):
    """

    :param disease: represents a string with disease
    :return: all the symptoms for that disease
    """

    df = pd.read_csv(
        r'C:\Users\Ofir\PycharmProjects\Cyber-Project2\Project\Server\DiseasesDatabases\symptom_precaution.csv').drop_duplicates(
        subset=['Disease'])

    advices = []
    for advice in [x for x in df.itertuples() if x[1]==disease]:
        print(advice)
        for i in range(2,6):
            advices.append(advice[i])

    return [x for x in advices if not pd.isna(x)]

















