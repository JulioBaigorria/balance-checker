import pandas as pd
import os
import time
import pandas as pd
import warnings


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
}
FILE_EXTENSIONS = '.csv'
FILE_EXTENSIONS2 = '.xlsx'
# Timer start
start = time.time()

# Funcion para hacer dinamica la importacion de excel y csv

def get_newest_file(file_prefix):
    files = os.listdir(INPUT_DIR)
    files = [file for file in files if file.startswith(
        file_prefix) and (file.endswith(FILE_EXTENSIONS) or file.endswith(FILE_EXTENSIONS2))]
    return max(files, key=lambda f: os.path.getmtime(os.path.join(INPUT_DIR, f)))

newest_imputaciones_file = get_newest_file(FILE_PREFIXES['imputaciones'])
newest_percepciones_file = get_newest_file(FILE_PREFIXES['percepciones'])
newest_retenciones_file = get_newest_file(FILE_PREFIXES['retenciones'])

# Importando DataFrames

imputaciones_df: pd.DataFrame = pd.read_csv(newest_imputaciones_file, sep=';', encoding='ISO8859-1', date_format=DATE_FORMAT, dtype=str)
percepciones_df: pd.DataFrame = pd.read_excel(newest_percepciones_file, skiprows=2)
retenciones_df: pd.DataFrame = pd.read_excel(newest_retenciones_file, skiprows=2)

    
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
