"""import os
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

newest_imputaciones_file = get_newest_file(FILE_PREFIXES['imputaciones'])
imputaciones_df: pd.DataFrame = pd.read_csv(newest_imputaciones_file, sep=';', encoding='ISO8859-1', date_format=DATE_FORMAT)
match_df: pd.DataFrame = pd.DataFrame()

match choice:
    case 1:
        newest_percepciones_file = get_newest_file(FILE_PREFIXES['percepciones'])
        imputaciones_df = pd.read_csv(newest_imputaciones_file, sep=';', encoding='ISO8859-1', date_format=DATE_FORMAT)
    case 2:
        newest_retenciones_file = get_newest_file(FILE_PREFIXES['retenciones'])
        retenciones_df = pd.read_excel(newest_retenciones_file, skiprows=2)
    case 3:
        newest_arba_file = get_newest_file(FILE_PREFIXES['arba'])
    case 4:
        newest_santafe_file = get_newest_file(FILE_PREFIXES['santafe'])
        
    case 5:
        newest_ganancias_file = get_newest_file(FILE_PREFIXES['ganancias'])
    case 6:
        newest_sicore_file = get_newest_file(FILE_PREFIXES['sicore'])


# Timer start
start = time.time()


newest_percepciones_file = get_newest_file(FILE_PREFIXES['percepciones'])


newest_santafe_file = get_newest_file(FILE_PREFIXES['santafe'])




# Importando DataFrames


percepciones_df: pd.DataFrame = pd.read_excel(newest_percepciones_file, skiprows=2)


    
# Procesando imputaciones_df

imputaciones_df['Debe'].dtypes

imputaciones_df['Emisión'] = pd.to_datetime(imputaciones_df['Emisión'], format="%d-%m-%Y")

imputaciones_df = imputaciones_df.sort_values(by='Emisión')
imputaciones_df[['Debe', 'Haber']] = imputaciones_df[['Debe', 'Haber']].map(lambda x : float(str(x).replace('.','').replace(',','.')))


imputaciones_df.to_excel('imputaciones_limpio.xlsx', index=False)

# Procesando percepciones_df

percepciones_df['Monto Percibido'] = abs(percepciones_df['Monto Percibido'])
retenciones_df['Monto Percibido'] = abs(percepciones_df['Monto Percibido'])

percepciones_df = percepciones_df[percepciones_df['Monto Percibido'] > 0]
retenciones_df = retenciones_df[retenciones_df['Monto Percibido'] > 0]


# Buscar coincidencias entre archivo Retencion y Percepcion
coincidencias_per = percepciones_df['Monto Percibido'].isin(imputaciones_df['Debe'])
percepciones_df[~coincidencias_per] # No estan
percepciones_df[coincidencias_per] # Si estan


coincidencias_ret = retenciones_df['Monto Retenido'].isin(imputaciones_df['Debe'])
retenciones_df[~coincidencias_ret] # No estan
retenciones_df[coincidencias_ret] # Si estan

excedente_imp = imputaciones_df[(~imputaciones_df['Debe'].isin(percepciones_df['Monto Percibido'])) & (~imputaciones_df['Debe'].isin(retenciones_df['Monto Retenido']))]
excedente_imp = excedente_imp[excedente_imp['Debe'] > 0]

try:
    with pd.ExcelWriter('resultados.xlsx', engine='openpyxl') as writer:
        # Sheet para Percepciones No Encontradas
        percepciones_df[~coincidencias_per].to_excel(writer, sheet_name='Perc No Encontradas', index=False)

        # Sheet para Retenciones No Encontradas
        retenciones_df[~coincidencias_ret].to_excel(writer, sheet_name='Ret No Encontradas', index=False)
        
        # Sheet para los Excendentes
        excedente_imp.to_excel(writer, sheet_name='Excedentes', index=False)
        
        # Sheet para Percepciones Encontradas
        percepciones_df[coincidencias_per].to_excel(writer, sheet_name='Perc Encontradas', index=False)

        # Sheet para Retenciones Encontradas
        retenciones_df[coincidencias_ret].to_excel(writer, sheet_name='Ret Encontradas', index=False)
        
        print('Archivos Generados!')
except BaseException as e:
    raise e

time.sleep(1)
print(f'{time.time() - start}')

"""