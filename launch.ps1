$PythonCommand = "python"
$PipCommand = "pip"
$VenvLocation = "window-magnifier-venv"

if (-Not(Get-Command $PythonCommand -errorAction SilentlyContinue)) {
    $PythonCommand = "python3"
}

if (-Not(Get-Command $PipCommand -errorAction SilentlyContinue)) {
    $PipCommand = "pip3"
}

if (-Not(Test-Path $VenvLocation)) {
    Invoke-Expression "$PythonCommand -m venv $VenvLocation"`
}

Invoke-Expression "./$VenvLocation/Scripts/Activate.ps1"`
    && Invoke-Expression "$PipCommand install -r requirements.txt"`
    && Invoke-Expression "$PythonCommand -m magnifier.start"