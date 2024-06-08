# Herramienta para búsqueda de datos

## Necesidad: 
El sector contable necesita mejorar sus tiempos de detección de montos para conciliaciones. Para esto se debe comparar la información obtenida entre el archivo ERP extraido y los distintos organismos recaudadores de impuestos.

## Como Usar:
- Hacer clic sobre el archivo "laucher.bat".
1. El launcher se encargara de crear un entorno virtual o abrir el existente y asi trabajar con las librerias de manera aislada.
2. Ejecuta el script main.py.
3. Cierra el entorno virtual.

- Si quiere realizar cambios en el archivo "main.py" solo se recomienda cambiar las constantes: NOMBRE_FORMULARIO, NOMBRE_IMPUTACIONES y TOLERANCIA.

![alt text](https://i.imgur.com/bHhHmAr.png)

- NO CAMBIAR la estructura de ninguna entrada o fuente de datos (Tanto ImputacionesPorSistemas.csv como FORMULARIO DE CARGA.xlsx)

## Entradas  y Fuente de Archivos:
- Archivo "imputacionesPorSistemas.csv". Sacado del ERP Integra.
- Archivo "FORMULARIO DE CARGA.xlsx". Plantilla utilizada para estandarizar los archivos Coprib, ARBA, SICORE, etc.

## Procedimiento:
El script toma ambas entradas, buscando coincidencias numericas desde el archivo "imputacionesPorSistemas.csv" en el "FORMULARIO DE CARGA.xlsx".
Los resultados se mostraron en un archivo llamado "Resultado.xlsx" creado en la carpeta raiz del script.

## Salida:
- Archivo llamado "Resultado.xlsx"

## Software principal utilizado:
- Python.
- Pandas. https://pypi.org/project/pandas/
- Openpyxl. https://pypi.org/project/openpyxl/
- PowerShell. Abrirlo por primera vez como administrador y colocar el siguiente comando: 

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```