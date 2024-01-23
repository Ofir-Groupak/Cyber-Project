import pandas as pd

df = pd.read_csv(r'C:\Users\Ofir\PycharmProjects\Cyber-Project\Diseases Databases\dataset.csv')

search_symptom = "Fever"

result = df[df.apply(lambda row: search_symptom in row.values, axis=1)]

print(result)






