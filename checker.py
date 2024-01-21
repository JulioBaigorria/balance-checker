import os
import time
import warnings
import pandas as pd

warnings.simplefilter("ignore")

# Constants
DATE_FORMAT = "%d-%m-%Y"
FLOAT_FORMAT = '%.3f'
INPUT_DIR = '.'
OUTPUT_DIR = '.'
FILE_PREFIXES = {
    'imputaciones': 'imputacionesPo',
    'percepciones': 'SrcPercepciones',
    'retenciones': 'SrcRetenciones',
    'arba': 'ARBA',
    'santafe': 'COPRIB - IIBB RET',
    'ganancias': 'GANANCIAS SUFRIDAS',
    'sicore': 'SICORE RET Y PERC IVA',
}

FILE_EXTENSIONS = '.csv'
FILE_EXTENSIONS2 = '.xlsx'
FILE_EXTENSIONS3 = '.xls'

OPTION_PREFIXES = {key: value for key, value in FILE_PREFIXES.items() if key != 'imputaciones'}
print("Elige una opción:")
for idx, option in enumerate(OPTION_PREFIXES.keys(), 1):
    print(f"{idx}. {option}")

choice = int(input("Opción: "))

# Dynamic function to get the latest needed files. 
def get_newest_file(file_prefix):
    files = os.listdir(INPUT_DIR)
    files = [file for file in files if file.startswith(
        file_prefix) and (file.endswith(FILE_EXTENSIONS) or file.endswith(FILE_EXTENSIONS2) or file.endswith(FILE_EXTENSIONS3))]
    return max(files, key=lambda f: os.path.getmtime(os.path.join(INPUT_DIR, f)))

# Functions for handling DFs
# Handling Imputaciones' file
def handle_imputaciones_df(imputaciones_df: pd.DataFrame) -> pd.DataFrame:
    imputaciones_df = imputaciones_df.drop(labels=['Unnamed: 8'], axis=1)
    imputaciones_df['Emisión'] = pd.to_datetime(imputaciones_df['Emisión'], format="%d-%m-%Y")
    imputaciones_df = imputaciones_df.sort_values(by='Emisión')
    imputaciones_df[['Debe', 'Haber']] = imputaciones_df[['Debe', 'Haber']].map(lambda x : float(str(x).replace('.','').replace(',','.')))
    imputaciones_df.to_excel('imputaciones_limpio.xlsx', index=False)
    return imputaciones_df

def handle_percepciones_df(percepciones_df: pd.DataFrame) -> pd.DataFrame:
    
    return percepciones_df

newest_imputaciones_file = get_newest_file(FILE_PREFIXES['imputaciones'])
imputaciones_df: pd.DataFrame = pd.read_csv(newest_imputaciones_file, sep=';', encoding='ISO8859-1', date_format=DATE_FORMAT)
cleaned_imputaciones_df = handle_imputaciones_df(imputaciones_df)
match_df: pd.DataFrame

match choice:
    case 1:
        newest_percepciones_file = get_newest_file(FILE_PREFIXES['percepciones'])
        match_df = pd.read_excel(newest_percepciones_file, skiprows=2)
        match_df = handle_percepciones_df(match_df)       
        print(newest_percepciones_file)
    case 2:
        newest_retenciones_file = get_newest_file(FILE_PREFIXES['retenciones'])
        match_df = pd.read_excel(newest_retenciones_file, skiprows=2)
        print(newest_retenciones_file)
    case 3:
        newest_arba_file = get_newest_file(FILE_PREFIXES['arba'])
        match_df = pd.read_excel(newest_arba_file, skiprows=2)
        print(newest_arba_file)
    case 4:
        newest_santafe_file = get_newest_file(FILE_PREFIXES['santafe'])
        match_df = pd.read_excel(newest_santafe_file, skiprows=2)
        print(newest_santafe_file)
    case 5:
        newest_ganancias_file = get_newest_file(FILE_PREFIXES['ganancias'])
        match_df = pd.read_excel(newest_ganancias_file, skiprows=2)
        print(newest_ganancias_file)
    case 6:
        newest_sicore_file = get_newest_file(FILE_PREFIXES['sicore'])
        match_df = pd.read_excel(newest_sicore_file, skiprows=2)
        print(newest_sicore_file)
    case _:
        print('Opcion No Valida')

print(cleaned_imputaciones_df)

# print(match_df.columns)
# print(match_df.dtypes)