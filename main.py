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
    'arba': 'planillaDeducciones',
    'santafe': 'COPRIB - IIBB RET',
    'ganancias': 'GANANCIAS SUFRIDAS',
    'sicore': 'SICORE RET Y PERC IVA',
    'percepciones_y_retenciones': ['SrcPercepciones', 'SrcRetenciones']
}
TOLERANCIA = 1.0
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
    cleaned_imputaciones_df['Haber'] = -cleaned_imputaciones_df['Haber']
    percepciones_df['Flag'] = False
    cleaned_imputaciones_df['Flag'] = False

    # Made List to be able to Flat through loop

    list_percepciones_df = percepciones_df.values
    list_cleaned_imputaciones_df = cleaned_imputaciones_df.values

    for i in list_cleaned_imputaciones_df:
        for p in list_percepciones_df:
            if abs(i[5] - p[13]) <= TOLERANCIA and i[9] == False and p[17] == False:
                i[9] = True
                p[17] = True

            elif abs(i[6] - p[13]) <= TOLERANCIA and i[9] == False and p[17] == False:
                i[9] = True
                p[17] = True

    df_resultado_per = pd.DataFrame(
        data=list_percepciones_df, columns=percepciones_df.columns)

    df_resultado_imputaciones_sobrantes = pd.DataFrame(
        data=list_cleaned_imputaciones_df, columns=cleaned_imputaciones_df.columns)

    # Percepciones
    print(
        # No estan
        f"Cantidad Percepciones No Encontradas: {df_resultado_per['Flag'][df_resultado_per['Flag'] == False].count()}")
    print(
        # Estan
        f"Cantidad Percepciones Encontradas:{df_resultado_per['Flag'][df_resultado_per['Flag']].count()}")
    # Sobrantes
    print(
        f"Cantidad Imputaciones Integra:{df_resultado_imputaciones_sobrantes['Flag'].count()}")
    print(
        f"Cantidad Sobrantes:{df_resultado_imputaciones_sobrantes['Flag'][df_resultado_imputaciones_sobrantes['Flag'] == False].count()}")

    print(
        f"Tolerancia de busqueda:{TOLERANCIA}")
    try:
        with pd.ExcelWriter('resultados_percepciones.xlsx', engine='openpyxl') as writer:
            # Sheet para Percepciones No Encontradas
            df_resultado_per[df_resultado_per['Flag'] == False].to_excel(
                writer, sheet_name='Perc No Encontradas', index=False)

            # Sheet para Percepciones Encontradas
            df_resultado_per[df_resultado_per['Flag']].to_excel(
                writer, sheet_name='Perc Encontradas', index=False)

            # Sheet para Sobrantes
            df_resultado_imputaciones_sobrantes[df_resultado_imputaciones_sobrantes['Flag'] == False].to_excel(
                writer, sheet_name='Sobrantes', index=False)

            print('Archivos Generados!')
            print(f'Tomó: {int(time.time() - start)} Segundos')
        time.sleep(5)
    except BaseException as e:
        time.sleep(10)
        raise e


def handle_search_retenciones_df(cleaned_imputaciones_df: pd.DataFrame, retenciones_df: pd.DataFrame) -> None:
    start = time.time()
    cleaned_imputaciones_df['Haber'] = -cleaned_imputaciones_df['Haber']

    retenciones_df['Flag'] = False
    cleaned_imputaciones_df['Flag'] = False

    list_retenciones_df = retenciones_df.values
    list_cleaned_imputaciones_df = cleaned_imputaciones_df.values

    for k in list_cleaned_imputaciones_df:
        for r in list_retenciones_df:
            if abs(k[5] - r[12]) <= TOLERANCIA and k[9] == False and r[17] == False:
                k[9] = True
                r[18] = True
            elif abs(k[6] - r[12]) <= TOLERANCIA and k[9] == False and r[17] == False:
                k[9] = True
                r[18] = True

    df_resultado_ret = pd.DataFrame(
        data=list_retenciones_df, columns=retenciones_df.columns)

    df_resultado_imputaciones_sobrantes = pd.DataFrame(
        data=list_cleaned_imputaciones_df, columns=cleaned_imputaciones_df.columns)

    # Test Retenciones
    # No encontradas
    df_resultado_ret['Flag'][df_resultado_ret['Flag'] == False].count()
    # Encontradas
    df_resultado_ret['Flag'][df_resultado_ret['Flag']].count()

    # Test Sobrantes
    df_resultado_imputaciones_sobrantes['Flag'][df_resultado_imputaciones_sobrantes['Flag'] == False].count(
    )
    df_resultado_imputaciones_sobrantes['Flag'][df_resultado_imputaciones_sobrantes['Flag']].count(
    )

    # Retenciones
    print(
        # No estan
        f"Cantidad Retenciones No Encontradas: {df_resultado_ret['Flag'][df_resultado_ret['Flag'] == False].count()}")
    print(
        # Estan
        f"Cantidad Retenciones Encontradas:{df_resultado_ret['Flag'][df_resultado_ret['Flag']].count()}")
    # Sobrantes
    print(
        f"Cantidad Imputaciones Integra:{df_resultado_imputaciones_sobrantes['Flag'].count()}")
    print(
        f"Cantidad Sobrantes:{df_resultado_imputaciones_sobrantes['Flag'][df_resultado_imputaciones_sobrantes['Flag'] == False].count()}")

    print(
        f"Tolerancia de busqueda:{TOLERANCIA}")
    
    try:
        with pd.ExcelWriter('resultados_percepciones_y_retenciones.xlsx', engine='openpyxl') as writer:
            # Sheet para Retenciones No Encontradas
            df_resultado_ret[df_resultado_ret['Flag'] == False].to_excel(
                writer, sheet_name='Ret No Encontradas', index=False)

            # Sheet para Retenciones Encontradas
            df_resultado_ret[df_resultado_ret['Flag']].to_excel(
                writer, sheet_name='Ret Encontradas', index=False)

            # Sheet para Sobrantes
            df_resultado_imputaciones_sobrantes[df_resultado_imputaciones_sobrantes['Flag'] == False].to_excel(
                writer, sheet_name='Sobrantes', index=False)

            print('Archivos Generados!')
            print(f'Tomó: {int(time.time() - start)} Segundos')
        time.sleep(5)
    except BaseException as e:
        time.sleep(10)
        raise e


def handle_search_arba_df(cleaned_imputaciones_df: pd.DataFrame, arba_df: pd.DataFrame) -> None:
    start = time.time()
    cleaned_imputaciones_df['Haber'] = -cleaned_imputaciones_df['Haber']

    encontradas_df = arba_df[
        arba_df['monto'].apply(
            lambda x: cleaned_imputaciones_df[['Debe', 'Haber']].apply(
                lambda col: col.between(x - TOLERANCIA, x + TOLERANCIA).any(), axis=1
            ).any()
        )
    ]
    cleaned_imputaciones_df['Haber'] = cleaned_imputaciones_df['Haber'] * -1

    no_encontradas_df = arba_df[~arba_df.index.isin(encontradas_df.index)]

    sobrantes_df = cleaned_imputaciones_df[~cleaned_imputaciones_df.index.isin(
        encontradas_df.index)]

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
    cleaned_imputaciones_df['Haber'] = -cleaned_imputaciones_df['Haber']

    encontradas_df = stafe_df[
        stafe_df['Importe'].apply(
            lambda x: cleaned_imputaciones_df[['Debe', 'Haber']].apply(
                lambda col: col.between(x - TOLERANCIA, x + TOLERANCIA).any(), axis=1
            ).any()
        )
    ]
    cleaned_imputaciones_df['Haber'] = cleaned_imputaciones_df['Haber'] * -1

    no_encontradas_df = stafe_df[~stafe_df.index.isin(encontradas_df.index)]

    sobrantes_df = cleaned_imputaciones_df[~cleaned_imputaciones_df.index.isin(
        encontradas_df.index)]

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
    cleaned_imputaciones_df['Haber'] = -cleaned_imputaciones_df['Haber']

    encontradas_df = ganancias_df[
        ganancias_df['Importe Ret./Perc.'].apply(
            lambda x: cleaned_imputaciones_df[['Debe', 'Haber']].apply(
                lambda col: col.between(x - TOLERANCIA, x + TOLERANCIA).any(), axis=1
            ).any()
        )
    ]
    cleaned_imputaciones_df['Haber'] = cleaned_imputaciones_df['Haber'] * -1

    no_encontradas_df = ganancias_df[~ganancias_df.index.isin(
        encontradas_df.index)]

    sobrantes_df = cleaned_imputaciones_df[~cleaned_imputaciones_df.index.isin(
        encontradas_df.index)]

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
    cleaned_imputaciones_df['Haber'] = -cleaned_imputaciones_df['Haber']

    encontradas_df = sicore_df[
        sicore_df['Importe Ret./Perc.'].apply(
            lambda x: cleaned_imputaciones_df[['Debe', 'Haber']].apply(
                lambda col: col.between(x - TOLERANCIA, x + TOLERANCIA).any(), axis=1
            ).any()
        )
    ]
    cleaned_imputaciones_df['Haber'] = cleaned_imputaciones_df['Haber'] * -1

    no_encontradas_df = sicore_df[~sicore_df.index.isin(encontradas_df.index)]

    sobrantes_df = cleaned_imputaciones_df[~cleaned_imputaciones_df.index.isin(
        encontradas_df.index)]

    # No estan
    print(
        f"Cantidad No encontradas:{no_encontradas_df['CUIT Agente Ret./Perc.'].count()}")

    # Estan
    print(
        f"Cantidad encontradas:{encontradas_df['CUIT Agente Ret./Perc.'].count()}")

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


def handle_search_percepciones_retenciones_df(cleaned_imputaciones_df: pd.DataFrame, percepciones_df: pd.DataFrame, retenciones_df: pd.DataFrame) -> None:
    start = time.time()

    cleaned_imputaciones_df['Haber'] = -cleaned_imputaciones_df['Haber']

    # Flag to avoid duplicates
    percepciones_df['Flag'] = False
    retenciones_df['Flag'] = False
    cleaned_imputaciones_df['Flag'] = False

    # Made List to be able to Flat through loop

    list_percepciones_df = percepciones_df.values
    list_retenciones_df = retenciones_df.values
    list_cleaned_imputaciones_df = cleaned_imputaciones_df.values

    for i in list_cleaned_imputaciones_df:
        for p in list_percepciones_df:
            if abs(i[5] - p[13]) <= TOLERANCIA and i[9] == False and p[17] == False:
                i[9] = True
                p[17] = True

            elif abs(i[6] - p[13]) <= TOLERANCIA and i[9] == False and p[17] == False:
                i[9] = True
                p[17] = True

    for k in list_cleaned_imputaciones_df:
        for r in list_retenciones_df:
            if abs(k[5] - r[12]) <= TOLERANCIA and k[9] == False and r[17] == False:
                k[9] = True
                r[18] = True
            elif abs(k[6] - r[12]) <= TOLERANCIA and k[9] == False and r[17] == False:
                k[9] = True
                r[18] = True

    df_resultado_per = pd.DataFrame(
        data=list_percepciones_df, columns=percepciones_df.columns)

    df_resultado_ret = pd.DataFrame(
        data=list_retenciones_df, columns=retenciones_df.columns)

    df_resultado_imputaciones_sobrantes = pd.DataFrame(
        data=list_cleaned_imputaciones_df, columns=cleaned_imputaciones_df.columns)

    # Test Percepciones
    # No encontradas
    df_resultado_per['Flag'][df_resultado_per['Flag'] == False].count()
    # Encontradas
    df_resultado_per['Flag'][df_resultado_per['Flag']].count()

    # Test Retenciones
    # No encontradas
    df_resultado_ret['Flag'][df_resultado_ret['Flag'] == False].count()
    # Encontradas
    df_resultado_ret['Flag'][df_resultado_ret['Flag']].count()

    # Test Sobrantes
    df_resultado_imputaciones_sobrantes['Flag'][df_resultado_imputaciones_sobrantes['Flag'] == False].count(
    )
    df_resultado_imputaciones_sobrantes['Flag'][df_resultado_imputaciones_sobrantes['Flag']].count(
    )

    # Percepciones
    print(
        # No estan
        f"Cantidad Percepciones No Encontradas: {df_resultado_per['Flag'][df_resultado_per['Flag'] == False].count()}")
    print(
        # Estan
        f"Cantidad Percepciones Encontradas:{df_resultado_per['Flag'][df_resultado_per['Flag']].count()}")
    # Retenciones
    print(
        # No estan
        f"Cantidad Retenciones No Encontradas: {df_resultado_ret['Flag'][df_resultado_ret['Flag'] == False].count()}")
    print(
        # Estan
        f"Cantidad Retenciones Encontradas:{df_resultado_ret['Flag'][df_resultado_ret['Flag']].count()}")
    # Sobrantes
    print(
        f"Cantidad Imputaciones Integra:{df_resultado_imputaciones_sobrantes['Flag'].count()}")
    print(
        f"Cantidad Sobrantes:{df_resultado_imputaciones_sobrantes['Flag'][df_resultado_imputaciones_sobrantes['Flag'] == False].count()}")

    print(
        f"Tolerancia de busqueda:{TOLERANCIA}")
    try:
        with pd.ExcelWriter('resultados_percepciones_y_retenciones.xlsx', engine='openpyxl') as writer:
            # Sheet para Percepciones No Encontradas
            df_resultado_per[df_resultado_per['Flag'] == False].to_excel(
                writer, sheet_name='Perc No Encontradas', index=False)

            # Sheet para Percepciones Encontradas
            df_resultado_per[df_resultado_per['Flag']].to_excel(
                writer, sheet_name='Perc Encontradas', index=False)

            # Sheet para Retenciones No Encontradas
            df_resultado_ret[df_resultado_ret['Flag'] == False].to_excel(
                writer, sheet_name='Ret No Encontradas', index=False)

            # Sheet para Retenciones Encontradas
            df_resultado_ret[df_resultado_ret['Flag']].to_excel(
                writer, sheet_name='Ret Encontradas', index=False)

            # Sheet para Sobrantes
            df_resultado_imputaciones_sobrantes[df_resultado_imputaciones_sobrantes['Flag'] == False].to_excel(
                writer, sheet_name='Sobrantes', index=False)

            print('Archivos Generados!')
            print(f'Tomó: {int(time.time() - start)} Segundos')
        time.sleep(5)
    except BaseException as e:
        time.sleep(10)
        raise e


newest_imputaciones_file = get_newest_file(FILE_PREFIXES['imputaciones'])
imputaciones_df: pd.DataFrame = pd.read_csv(
    newest_imputaciones_file, sep=';', encoding='latin-1', date_format=DATE_FORMAT)
cleaned_imputaciones_df = handle_imputaciones_df(imputaciones_df)


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
    case 7:
        newest_percepciones_file = get_newest_file(
            FILE_PREFIXES['percepciones'])
        newest_retenciones_file = get_newest_file(FILE_PREFIXES['retenciones'])
        percepciones_df = pd.read_excel(newest_percepciones_file, skiprows=2)
        retenciones_df = pd.read_excel(newest_retenciones_file, skiprows=2)
        handle_search_percepciones_retenciones_df(
            cleaned_imputaciones_df, percepciones_df, retenciones_df)
    case _:
        print('Opcion No Valida')


time.sleep(3)