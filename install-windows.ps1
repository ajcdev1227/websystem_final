# NOTICE:
# Before running this, create a venv and use the Activate script to get a shell from within the venv context.
# Once you're within the venv context, run this script.
# It may require running as administrator because creation of symbolic links is restricted by default.

# === Config ===

$PYTHON = "python"
$PIP = "pip"

# === Code ===

# Get the directory of the current script
$SCRIPT_DIR = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

# Change directory to the script directory
Set-Location $SCRIPT_DIR



# Determine the Lib directory dynamically
$LIBDIR = (Get-ChildItem env\Lib\site-packages\ -Directory | Select-Object -First 1).FullName



Write-Host "Installing dependencies inside venv..."
& $PIP install -r requirements.txt

Write-Host "Symlinking wagtail libraries..."
$wagtailDirs = Get-ChildItem -Path "$SCRIPT_DIR" -Directory | Where-Object { $_.Name -match '^wagtail' }
foreach ($dir in $wagtailDirs) {
    $targetPath = Join-Path -Path $LIBDIR -ChildPath $dir.Name
    if (Test-Path $targetPath) {
        Remove-Item $targetPath -Force -Recurse
    }
    New-Item -ItemType SymbolicLink -Path $LIBDIR -Name $dir.Name -Value $dir.FullName
}

Write-Host "Running migrations..."
& $PYTHON manage.py migrate_schemas --shared

Write-Host "Creating seed data..."
& $PYTHON manage.py loaddata "$SCRIPT_DIR\seed\multi.json"

Write-Host "=================================================================================="
Write-Host "Packages have been installed through pip, and custom versions have been symlinked."
Write-Host "Run the following to launch an interactive PowerShell prompt inside the venv:"
Write-Host ". .\venv\Scripts\Activate.ps1"
