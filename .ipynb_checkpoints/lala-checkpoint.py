import pandas as pd

# Charger le premier fichier Excel
df = pd.read_csv('data.csv')

# Charger le fichier de mapping des noms de colonnes
mapping_df = pd.read_excel('Mapping_noms_variables_sphinx.xlsx')

# Créer un dictionnaire à partir du dataframe de mapping
# Assure-toi que les colonnes sont nommées correctement dans le fichier Excel
column_mapping = dict(zip(mapping_df['Anciens Noms'], mapping_df['Nouveaux Noms']))

# Renommer les colonnes dans le dataframe principal
df.rename(columns=column_mapping, inplace=True)

# Afficher le dataframe modifié pour vérifier
print(df.head())
df.to_csv('nouveau_fichier.csv', index=False)
