import time
import warnings
import pandas as pd


start = time.time()

warnings.simplefilter("ignore")

# Constants
DATE_FORMAT = "%d-%m-%Y"
FLOAT_FORMAT = '%.3f'
TOLERANCIA = 1.0

formulario_df: pd.DataFrame = pd.read_excel(
    'MODELO DE FORMULARIO DE CARGA.xlsx')
imputaciones_df: pd.DataFrame = pd.read_csv(
    'imputacionesPorSistemas.csv', sep=';', encoding='latin-1', date_format=DATE_FORMAT)


def handle_imputaciones_df(imputaciones_df: pd.DataFrame) -> pd.DataFrame:
    imputaciones_df[['Debe', 'Haber']] = imputaciones_df[['Debe', 'Haber']].map(
        lambda x: float(str(x).replace('.', '').replace(',', '.')))
    return imputaciones_df


cleaned_imputaciones_df = handle_imputaciones_df(imputaciones_df)

cleaned_imputaciones_df['Haber'] = -cleaned_imputaciones_df['Haber']

formulario_df['Flag'] = False
cleaned_imputaciones_df['Flag'] = False

list_formulario_df = formulario_df.values
list_cleaned_imputaciones_df = cleaned_imputaciones_df.values


for i in list_cleaned_imputaciones_df:
    for p in list_formulario_df:
        if abs(i[5] - p[4]) <= TOLERANCIA and i[9] == False and p[6] == False:
            i[9] = True
            p[6] = True

        elif abs(i[6] - p[4]) <= TOLERANCIA and i[9] == False and p[6] == False:
            i[9] = True
            p[6] = True


resultado_formulario_df = pd.DataFrame(
    data=list_formulario_df, columns=formulario_df.columns)

resultado_imputaciones_df = pd.DataFrame(
    data=list_cleaned_imputaciones_df, columns=cleaned_imputaciones_df.columns)

resultado_imputaciones_df['Haber'] = resultado_imputaciones_df['Haber'] * -1

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
