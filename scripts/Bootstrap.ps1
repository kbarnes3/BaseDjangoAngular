# Resolve all dependencies that the project requires to run.
param(
    [switch]$Verbose
)

. $PSScriptRoot\Write-Status.ps1

if ($Verbose) {
    $quiet = $null
}
else {
    $quiet = "--quiet"
}

$project_root = Split-Path $PSScriptRoot

Push-Location $project_root

if (-Not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Status "Installing uv"
    & winget install --id astral-sh.uv -e
}

Write-Status "Updating Python requirements"
& uv sync

$already_activated = . $PSScriptRoot\Ensure-Venv.ps1
Write-Status "Updating npm"
. $PSScriptRoot\Invoke-Npm.ps1 @('install', '--location=global', 'npm@12')
Write-Status "Updating Angular CLI"
. $PSScriptRoot\Invoke-Npm.ps1 @('install', '--location=global', '@angular/cli')
Write-Status "Updating Node requirements"
. $PSScriptRoot\Invoke-Npm.ps1 @('install')

if ($Global:console_functions) {
    # Define or update the console scripts if we want them
    . $PSScriptRoot\Console-Scripts.ps1
}

Pop-Location

if (-Not $already_activated) {
    deactivate
}
