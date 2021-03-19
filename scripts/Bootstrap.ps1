# Resolve all dependencies that the project requires to run.
param(
    [switch]$Verbose
)

. $PSScriptRoot\Write-Status.ps1

if ($Verbose) {
    $quiet = ""
}
else {
    $quiet = "--quiet"
}

$project_root = Split-Path $PSScriptRoot

Push-Location $project_root

$venv = Join-Path $project_root "venv"
if (-Not (Test-Path $venv)) {
    Write-Status "Creating venv in $venv"
    & py -3.6 -m venv $venv
}

$already_activated = . $PSScriptRoot\Ensure-Venv.ps1

Write-Status "Updating pip"
& python -m pip install --upgrade pip $quiet
Write-Status "Updating requirements"
& pip install -r (Join-Path $project_root "requirements.txt") $quiet
Write-Status "Updating dev-requirements"
& pip install -r (Join-Path $project_root "dev-requirements.txt") $quiet
Write-Status "Updating npm"
. $PSScriptRoot\Invoke-Npm @('install', '-g', 'npm@6')
Write-Status "Updating Angular CLI"
. $PSScriptRoot\Invoke-Npm @('install', '-g', '@angular/cli')t
Write-Status "Updating requirements"
. $PSScriptRoot\Invoke-Npm @('install')

if ($Global:console_functions) {
    # Define or update the console scripts if we want them
    . $PSScriptRoot\Console-Scripts.ps1
}

Pop-Location

if (-Not $already_activated) {
    deactivate
}
