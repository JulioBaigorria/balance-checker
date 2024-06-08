@echo off
REM Verificar si la carpeta .venv existe
IF NOT EXIST ".venv" (
    echo La carpeta .venv no existe, creando y configurando el entorno virtual...
    python -m venv .venv || PAUSE
    echo Instalando dependencias desde requirements.txt...
    .venv\Scripts\pip install -r requirements.txt || PAUSE
)

REM Activar el entorno virtual
echo Activando el entorno virtual...
call .venv\Scripts\activate || PAUSE

REM Ejecutar el script main.py
echo Ejecutando main.py...
python main.py || PAUSE

REM Desactivar el entorno virtual
echo Desactivando el entorno virtual...
call .venv\Scripts\deactivate || PAUSE

