$CurrentFolder = Get-Location | Split-Path -Leaf
$VenvLocation = "$CurrentFolder-venv"
Invoke-Expression "./$VenvLocation/Scripts/Activate.ps1"

$PipCommand = "pip"

if (-Not(Get-Command $PipCommand -errorAction SilentlyContinue)) {
    $PipCommand = "pip3"
}

Invoke-Expression "$PipCommand install pyinstaller"
Invoke-Expression "pyinstaller ./magnifier/start.py --windowed --icon=./magnifier/resources/icon.png --name=window-magnifier"
