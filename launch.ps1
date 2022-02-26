$pythonCommand = "python"
$pipCommand = "pip"

if (-Not(Get-Command $pythonCommand -errorAction SilentlyContinue)) {
    $pythonCommand = "python3"
}

if (-Not(Get-Command $pipCommand -errorAction SilentlyContinue)) {
    $pipCommand = "pip3"
}

Invoke-Expression "$pythonCommand -m venv window-magnifier-env"`
    && Invoke-Expression "./window-magnifier-env/Scripts/Activate.ps1"`
    && Invoke-Expression "$pipCommand install -r requirements.txt"`
    && Invoke-Expression "$pythonCommand -m magnifier.start"