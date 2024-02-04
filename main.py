import os
import time
import warnings
import pandas as pd

warnings.simplefilter("ignore")

# Constantes
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

OPTION_PREFIXES = {key: value for key,
                   value in FILE_PREFIXES.items() if key != 'imputaciones'}

print("Elige una opción:")
for idx, option in enumerate(OPTION_PREFIXES.keys(), 1):
    print(f"{idx}. {option}")

choice = int(input("Opción: "))

# Funcion para traer el ultimo archivo


def get_newest_file(file_prefix):
    files = os.listdir(INPUT_DIR)
    files = [file for file in files if file.startswith(
        file_prefix) and (file.endswith(FILE_EXTENSIONS) or file.endswith(FILE_EXTENSIONS2) or file.endswith(FILE_EXTENSIONS3))]
    return max(files, key=lambda f: os.path.getmtime(os.path.join(INPUT_DIR, f)))

################### FUNCIONES PARA MANEJAR LOS DISTINTOS ARCHIVOS #########################
# Se encuentra la logica de cada una de las opciones.

# Imputaciones


def handle_imputaciones_df(imputaciones_df: pd.DataFrame) -> pd.DataFrame:
    imputaciones_df[['Debe', 'Haber']] = imputaciones_df[['Debe', 'Haber']].map(
        lambda x: float(str(x).replace('.', '').replace(',', '.')))
    return imputaciones_df

# Percepciones


def handle_search_percepciones_df(cleaned_imputaciones_df: pd.DataFrame, percepciones_df: pd.DataFrame) -> None:
    start = time.time()
    # Buscar coincidencias de montos en Debe y Haber
    coincidencias_per = (percepciones_df['Monto Percibido'].isin(
        cleaned_imputaciones_df['Debe']) | percepciones_df['Monto Percibido'].isin(cleaned_imputaciones_df['Haber']))
    sobrantes_df = cleaned_imputaciones_df[~cleaned_imputaciones_df['Debe'].isin(
        percepciones_df['Monto Percibido']) & ~cleaned_imputaciones_df['Haber'].isin(percepciones_df['Monto Percibido'])]
    no_encontradas_df = percepciones_df[~coincidencias_per]
    encontradas_df = percepciones_df[coincidencias_per]

    print(
        # No estan
        f"Cantidad No Encontradas: {no_encontradas_df['CUIT'].count()}")
    print(f"Cantidad Encontradas:{encontradas_df['CUIT'].count()}")  # Estan
    print(f"Cantidad Sobrantes:{sobrantes_df.shape[0]}")  # Sobrantes

    try:
        with pd.ExcelWriter('resultados_percepciones.xlsx', engine='openpyxl') as writer:
            # Sheet para Percepciones No Encontradas
            no_encontradas_df.to_excel(
                writer, sheet_name='Perc No Encontradas', index=False)

            # Sheet para Percepciones Encontradas
            encontradas_df.to_excel(
                writer, sheet_name='Perc Encontradas', index=False)

            # Sheet para Sobrantes
            sobrantes_df.to_excel(
                writer, sheet_name='Sobrantes', index=False)

            print('Archivos Generados!')
        time.sleep(1)
    except BaseException as e:
        time.sleep(10)
        raise e

    print(f'Tomó: {int(time.time() - start)} Segundos')


def handle_search_retenciones_df(cleaned_imputaciones_df: pd.DataFrame, retenciones_df: pd.DataFrame) -> None:
    start = time.time()
    # Buscar coincidencias de montos en Debe y Haber
    coincidencias_ret = (retenciones_df['Monto Retenido'].isin(cleaned_imputaciones_df['Debe']) |
                         retenciones_df['Monto Retenido'].isin(cleaned_imputaciones_df['Haber']))
    # Se pregunta al reves ya que se devuelve imputaciones como sobrantes
    sobrantes_df = cleaned_imputaciones_df[~cleaned_imputaciones_df['Debe'].isin(
        retenciones_df['Monto Retenido']) & ~cleaned_imputaciones_df['Haber'].isin(retenciones_df['Monto Retenido'])]

    no_encontradas_df = retenciones_df[~coincidencias_ret]
    encontradas_df = retenciones_df[coincidencias_ret]

    # No estan
    print(
        f"Cantidad No Encontradas:{no_encontradas_df['CUIT'].count()}")
    # Estan
    print(f"Cantidad Encontradas:{encontradas_df['CUIT'].count()}")
    # Sobrantes
    print(f"Cantidad Sobrantes:{sobrantes_df.shape[0]}")

    try:
        with pd.ExcelWriter('resultados_retenciones.xlsx', engine='openpyxl') as writer:
            # Sheet para Percepciones No Encontradas
            no_encontradas_df.to_excel(
                writer, sheet_name='Ret No Encontradas', index=False)

            # Sheet para Percepciones Encontradas
            encontradas_df.to_excel(
                writer, sheet_name='Ret Encontradas', index=False)

            # Sheet para Sobrantes
            sobrantes_df.to_excel(
                writer, sheet_name='Sobrantes', index=False)

            print('Archivos Generados!')
        time.sleep(1)
    except BaseException as e:
        time.sleep(10)
        raise e

    print(f'Tomó: {int(time.time() - start)} Segundos')


def handle_search_arba_df(cleaned_imputaciones_df: pd.DataFrame, arba_df: pd.DataFrame) -> None:
    start = time.time()
    arba_df.describe()

    coincidencias_arba = (arba_df['monto'].isin(
        cleaned_imputaciones_df['Debe']) | arba_df['monto'].isin(cleaned_imputaciones_df['Haber']))

    sobrantes_df = cleaned_imputaciones_df[~cleaned_imputaciones_df['Debe'].isin(
        arba_df['monto']) & ~cleaned_imputaciones_df['Haber'].isin(arba_df['monto'])]

    no_encontradas_df = arba_df[~coincidencias_arba]
    encontradas_df = arba_df[coincidencias_arba]

    # No estan
    print(
        f"Cantidad No encontradas:{no_encontradas_df['cuit'].count()}")
    # Estan
    print(f"Cantidad encontradas:{encontradas_df['cuit'].count()}")
    # Sobrantes
    print(f"Cantidad Sobrantes:{sobrantes_df.shape[0]}")

    try:
        with pd.ExcelWriter('resultados_arba.xlsx', engine='openpyxl') as writer:
            # Sheet para Percepciones No Encontradas
            no_encontradas_df.to_excel(
                writer, sheet_name='Ret No Encontradas', index=False)

            # Sheet para Percepciones Encontradas
            encontradas_df.to_excel(
                writer, sheet_name='Ret Encontradas', index=False)

            # Sheet para Sobrantes
            sobrantes_df.to_excel(
                writer, sheet_name='Sobrantes', index=False)

            print('Archivos Generados!')
        time.sleep(1)
    except BaseException as e:
        time.sleep(10)
        raise e
    print(f'Tomó: {int(time.time() - start)} Segundos')


def handle_search_stafe_df(cleaned_imputaciones_df: pd.DataFrame, stafe_df: pd.DataFrame) -> None:
    start = time.time()

    coincidencias_stafe = (stafe_df['Importe'].isin(cleaned_imputaciones_df['Debe']) |
                           stafe_df['Importe'].isin(cleaned_imputaciones_df['Haber']))

    sobrantes_df = cleaned_imputaciones_df[~cleaned_imputaciones_df['Debe'].isin(
        stafe_df['Importe']) & ~cleaned_imputaciones_df['Haber'].isin(stafe_df['Importe'])]

    no_encontradas_df = stafe_df[~coincidencias_stafe]
    encontradas_df = stafe_df[coincidencias_stafe]

    # No estan
    print(
        f"Cantidad No encontradas:{no_encontradas_df['Cuit'].count()}")

    # Estan
    print(f"Cantidad encontradas:{encontradas_df['Cuit'].count()}")

    # Sobrantes
    print(f"Cantidad Sobrantes:{sobrantes_df.shape[0]}")

    try:
        with pd.ExcelWriter('resultados_santafe.xlsx', engine='openpyxl') as writer:
            # Sheet para Percepciones No Encontradas
            no_encontradas_df.to_excel(
                writer, sheet_name='Ret No Encontradas', index=False)

            # Sheet para Percepciones Encontradas
            encontradas_df.to_excel(
                writer, sheet_name='Ret Encontradas', index=False)

            # Sheet para Sobrantes
            sobrantes_df.to_excel(
                writer, sheet_name='Sobrantes', index=False)

            print('Archivos Generados!')
        time.sleep(1)
    except BaseException as e:
        time.sleep(10)
        raise e
    print(f'Tomó: {int(time.time() - start)} Segundos')


def handle_search_ganancias_df(cleaned_imputaciones_df: pd.DataFrame, ganancias_df: pd.DataFrame) -> None:
    start = time.time()
    coincidencias_ganancias = (ganancias_df['Importe Ret./Perc.'].isin(cleaned_imputaciones_df['Debe']) |
                               ganancias_df['Importe Ret./Perc.'].isin(cleaned_imputaciones_df['Haber']))

    sobrantes_df = cleaned_imputaciones_df[~cleaned_imputaciones_df['Debe'].isin(
        ganancias_df['Importe Ret./Perc.']) & ~cleaned_imputaciones_df['Haber'].isin(ganancias_df['Importe Ret./Perc.'])]

    no_encontradas_df = ganancias_df[~coincidencias_ganancias]
    encontradas_df = ganancias_df[coincidencias_ganancias]

    # No estan
    print(
        f"Cantidad No encontradas:{no_encontradas_df['CUIT Agente Ret./Perc.'].count()}")

    # Estan
    print(
        f"Cantidad encontradas:{encontradas_df['CUIT Agente Ret./Perc.'].count()}")

    # Sobrantes
    print(f"Cantidad Sobrantes:{sobrantes_df.shape[0]}")

    try:
        with pd.ExcelWriter('resultados_ganancias.xlsx', engine='openpyxl') as writer:
            # Sheet para Percepciones No Encontradas
            no_encontradas_df.to_excel(
                writer, sheet_name='Ret No Encontradas', index=False)

            # Sheet para Percepciones Encontradas
            encontradas_df.to_excel(
                writer, sheet_name='Ret Encontradas', index=False)

            # Sheet para Sobrantes
            sobrantes_df.to_excel(
                writer, sheet_name='Sobrantes', index=False)

            print('Archivos Generados!')
        time.sleep(1)
    except BaseException as e:
        time.sleep(10)
        raise e
    print(f'Tomó: {int(time.time() - start)} Segundos')


def handle_search_sicore_df(cleaned_imputaciones_df: pd.DataFrame, sicore_df: pd.DataFrame) -> None:
    start = time.time()
    coincidencias_sicore = (sicore_df['Importe Ret./Perc.'].isin(cleaned_imputaciones_df['Debe']) |
                            sicore_df['Importe Ret./Perc.'].isin(cleaned_imputaciones_df['Haber']))
    
    sobrantes_df = cleaned_imputaciones_df[~cleaned_imputaciones_df['Debe'].isin(
        sicore_df['Importe Ret./Perc.']) & ~cleaned_imputaciones_df['Haber'].isin(sicore_df['Importe Ret./Perc.'])]

    no_encontradas_df = sicore_df[~coincidencias_sicore]
    encontradas_df = sicore_df[coincidencias_sicore]
    
    # No estan
    print(f"Cantidad No encontradas:{no_encontradas_df['CUIT Agente Ret./Perc.'].count()}")
    
    # Estan
    print(f"Cantidad encontradas:{encontradas_df['CUIT Agente Ret./Perc.'].count()}")
    
    # Sobrantes
    print(f"Cantidad Sobrantes:{sobrantes_df.shape[0]}")

    try:
        with pd.ExcelWriter('resultados_sicore.xlsx', engine='openpyxl') as writer:
            # Sheet para Percepciones No Encontradas
            no_encontradas_df.to_excel(
                writer, sheet_name='Ret No Encontradas', index=False)

            # Sheet para Percepciones Encontradas
            encontradas_df.to_excel(
                writer, sheet_name='Ret Encontradas', index=False)
            
            # Sheet para Sobrantes
            sobrantes_df.to_excel(
                writer, sheet_name='Sobrantes', index=False)

            print('Archivos Generados!')
        time.sleep(1)
    except BaseException as e:
        time.sleep(10)
        raise e
    print(f'Tomó: {int(time.time() - start)} Segundos')


newest_imputaciones_file = get_newest_file(FILE_PREFIXES['imputaciones'])
imputaciones_df: pd.DataFrame = pd.read_csv(
    newest_imputaciones_file, sep=';', encoding='latin-1', date_format=DATE_FORMAT)
cleaned_imputaciones_df = handle_imputaciones_df(imputaciones_df)
match_df: pd.DataFrame = pd.DataFrame()


match choice:
    case 1:
        newest_percepciones_file = get_newest_file(
            FILE_PREFIXES['percepciones'])
        percepciones_df = pd.read_excel(newest_percepciones_file, skiprows=2)
        handle_search_percepciones_df(cleaned_imputaciones_df, percepciones_df)

    case 2:
        newest_retenciones_file = get_newest_file(FILE_PREFIXES['retenciones'])
        retenciones_df = pd.read_excel(newest_retenciones_file, skiprows=2)
        handle_search_retenciones_df(cleaned_imputaciones_df, retenciones_df)
    case 3:
        newest_arba_file = get_newest_file(FILE_PREFIXES['arba'])
        arba_df = pd.read_excel(newest_arba_file, skiprows=3, header=None, names=[
            'cuit', 'fecha', 'tipo', 'cond_iva', 'pv', 'no_se', 'monto_total', 'no_se1', 'monto', 'no_se2',
        ])
        handle_search_arba_df(cleaned_imputaciones_df, arba_df)
    case 4:
        newest_santafe_file = get_newest_file(FILE_PREFIXES['santafe'])
        stafe_df = pd.read_excel(newest_santafe_file, skiprows=2)
        handle_search_stafe_df(cleaned_imputaciones_df, stafe_df)
    case 5:
        newest_ganancias_file = get_newest_file(FILE_PREFIXES['ganancias'])
        ganancias_df = pd.read_excel(newest_ganancias_file)
        handle_search_ganancias_df(cleaned_imputaciones_df, ganancias_df)
    case 6:
        newest_sicore_file = get_newest_file(FILE_PREFIXES['sicore'])
        sicore_df = pd.read_excel(newest_sicore_file)
        handle_search_sicore_df(cleaned_imputaciones_df, sicore_df)
    case _:
        print('Opcion No Valida')
