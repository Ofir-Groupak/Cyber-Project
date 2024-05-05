import pandas
import pandas as pd

df = pd.read_csv(r'C:\Users\Ofir\PycharmProjects\Cyber-Project2\Project\Server\DiseasesDatabases\dataset.csv')

def get_diseases_with_symptom(symptom):
    """
    :param symptom:represents a string to a symptom
    :return:list of that symptom
    """
    lst = []

    for disease in df.itertuples():
        for i in range(2,17):
            try:
                if not pd.isna(disease[i]):
                    if disease[i].find(symptom)!=-1:
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
def possible_scenarios_for_disease(disease):
    """

    :param disease: represents a string with disease
    :return: all the symptoms for that disease
    """
    symptoms = []
    scenarios = []

    for line in [x for x in df.itertuples() if x[1]==disease]:
        for i in range(2,17):
            if line[i]!=None:
                symptoms.append(line[i])
        if symptoms not in scenarios:
            scenarios.append(symptoms)
        symptoms=[]

    return scenarios
def get_symptoms_for_disease(disease):
    """

    :param disease: represents a string with disease
    :return: all the symptoms for that disease
    """
    symptoms = []
    for symptom in [x for x in df.itertuples() if x[1]==disease]:
        for i in range(2,17):
            symptoms.append(symptom[i])

    return [x for x in symptoms if not pd.isna(x)]
def remove_scenarios_with_x(scenarios,symptom):
    """
    :param diseases: represents a dictionary with diseases and their symptoms
    :param symptom:represents a given stirng with symptom
    :return: a dictionary without diseases with certain symptom
    """
    updated_scenarios = []
    for scenario in scenarios:
        if symptom not in [x for x in scenario if not pandas.isna(x)]:
            updated_scenarios.append(scenario)
    return updated_scenarios

def remove_scenarios_without_x(scenarios, symptom):
    """
    :param diseases: represents a dictionary with diseases and their symptoms
    :param symptom:represents a given stirng with symptom
    :return: a dictionary with diseases with certain symptom
    """
    updated_scenarios = []
    print(scenarios)
    for scenario in scenarios:
        print(scenario)
        if symptom in [x for x in scenario if not pandas.isna(x)]:
            updated_scenarios.append(scenario)
    return updated_scenarios

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
        for i in range(2,6):
            advices.append(advice[i])

    return [x for x in advices if not pd.isna(x)]



def get_disease_by_symptoms(symptoms):
    # Read the Excel file into a DataFrame

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        disease_symptoms = row[1:]  # Exclude the first column (disease name)

        # Check if all symptoms for the current disease are present in the input symptoms
        if all(symptom in symptoms for symptom in disease_symptoms):
            return row[0]  # Return the disease name

    return "Unknown"  # Return "Unknown" if no matching disease is found

def get_next_symptom(scenario,user_symptoms):

    print(scenario)
    print('1',[x for x in scenario if not pd.isna(x)])
    for symptom in [x for x in scenario if not pd.isna(x)]:
        if not pandas.isna(symptom) and symptom not in user_symptoms:
            print(symptom)
            return symptom
    return ""

def get_diseases_by_scenarios(scenarios):

    diseases = []
    for scenario in scenarios:
        #print(scenario)
        diseases.append(get_disease_by_symptoms(scenario))

    return list(dict.fromkeys(diseases))









