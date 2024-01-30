# Verificar si el entorno virtual está instalado
$venvPath = ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Instalando entorno virtual..."
    python -m venv $venvPath

    # Activar el entorno virtual después de la instalación
    $activateScript = Join-Path $venvPath "Scripts\Activate"
    cmd /c $activateScript

    # Instalar dependencias desde requirements.txt
    Write-Host "Instalando dependencias..."
    python -m pip install -r requirements.txt
} else {
    # Activar el entorno virtual si ya está instalado
    $activateScript = Join-Path $venvPath "Scripts\Activate"
    cmd /c $activateScript
}

# Ejecutar el archivo main.py
Write-Host "Ejecutando main.py..."
python main.py

# Sleep
Start-Sleep 4