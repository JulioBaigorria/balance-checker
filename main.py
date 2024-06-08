import time
import warnings
import pandas as pd


start = time.time()

warnings.simplefilter("ignore")

# Constantes
DATE_FORMAT = "%d-%m-%Y"
FLOAT_FORMAT = '%.3f'
TOLERANCIA = 1.0


"""
    Constantes para los nombres de Archivos. Respetar las comillas y la extensiones de los archivos.
    El formulario es '.xlsx', el archivo de imputaciones es '.csv'.
"""
NOMBRE_FORMULARIO = 'FORMULARIO DE CARGA.xlsx'

NOMBRE_IMPUTACIONES = 'imputacionesPorSistemas.csv'

# Tolerancia de busqueda.
TOLERANCIA = 1.0


# Carga de los dos archivos "FORMULARIO DE CARGA" e "IMPUTACIONES POR SISTEMA".
formulario_df: pd.DataFrame = pd.read_excel(NOMBRE_FORMULARIO)
imputaciones_df: pd.DataFrame = pd.read_csv(NOMBRE_IMPUTACIONES, sep=';', encoding='latin-1', date_format=DATE_FORMAT)

# Funcion para Limpiar el Archivo de IMPUTACIONES POR SISTEMA.
def handle_imputaciones_df(imputaciones_df: pd.DataFrame) -> pd.DataFrame:
    imputaciones_df[['Debe', 'Haber']] = imputaciones_df[['Debe', 'Haber']].map(
        lambda x: float(str(x).replace('.', '').replace(',', '.')))
    return imputaciones_df

# Funcion para la busqueda de los registros.
def busqueda(cleaned_imputaciones_df):
    for i in list_cleaned_imputaciones_df:
        for p in list_formulario_df:
            if abs(i[5] - p[4]) <= TOLERANCIA and i[9] == False and p[6] == False:
                i[9] = True
                p[6] = True

            elif abs(i[6] - p[4]) <= TOLERANCIA and i[9] == False and p[6] == False:
                i[9] = True
                p[6] = True 
                
cleaned_imputaciones_df = handle_imputaciones_df(imputaciones_df)

# Convertir lo que es Haber en numero negativo para ser encontrado en el Formulario de Carga.
cleaned_imputaciones_df['Haber'] = -cleaned_imputaciones_df['Haber']

# Flags para saber si fueron encontrados o no.
formulario_df['Flag'] = False
cleaned_imputaciones_df['Flag'] = False

# Pasar los valores como listas para poder ser buscados como tales por la funcion "busqueda"
list_formulario_df = formulario_df.values
list_cleaned_imputaciones_df = cleaned_imputaciones_df.values

# Busqueda utilizando la funcion busqueda.
busqueda(list_formulario_df)

# Crea los Dataframes para poder ser exportados a Excel.
resultado_formulario_df = pd.DataFrame(
    data=list_formulario_df, columns=formulario_df.columns)

resultado_imputaciones_df = pd.DataFrame(
    data=list_cleaned_imputaciones_df, columns=cleaned_imputaciones_df.columns)


resultado_imputaciones_df['Haber'] = resultado_imputaciones_df['Haber'] * -1

# Exportacion de las variables
with pd.ExcelWriter('Resultado.xlsx', engine='openpyxl') as writer:
    # Sheet para las no encontradas
    resultado_formulario_df[resultado_formulario_df['Flag'] == False].to_excel(
        writer, sheet_name='No Encontradas', index=False)

    # Sheet para Percepciones Encontradas
    resultado_formulario_df[resultado_formulario_df['Flag']].to_excel(
        writer, sheet_name='Encontradas', index=False)

    # Sheet para Sobrantes
    resultado_imputaciones_df[resultado_imputaciones_df['Flag'] == False].to_excel(
        writer, sheet_name='Sobrantes', index=False)

    print('Archivos Generados!')
    print(f'Tomó: {int(time.time() - start)} Segundos')
