# Verificar si el entorno virtual está instalado
if (-not (Test-Path .venv)) {
    Write-Host "Instalando entorno virtual..."
    python -m venv .venv
}

# Activar el entorno virtual
.venv\Scripts\Activate

# Instalar dependencias (opcional, dependiendo de tus necesidades)
# pip install -r requirements.txt

# Ejecutar el archivo main.py
python main.py

# Desactivar el entorno virtual al finalizar
deactivate