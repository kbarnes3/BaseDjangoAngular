# This script updates the project to run for its current checkout.
param(
    [switch]$Verbose
)

. $PSScriptRoot\Write-Status.ps1
$project_root = Split-Path $PSScriptRoot
$already_activated = . $PSScriptRoot\Ensure-Venv.ps1

# Check Python version
$venv_version = & python --version
$installed_version = . $PSScriptRoot\Invoke-NonVenvPython.ps1 @('--version')
if (-Not $venv_version.StartsWith('Python 3.12')) {
    deactivate
    . $PSScriptRoot\Setup.ps1 -Verbose:$Verbose
    . $PSScriptRoot\Ensure-Venv.ps1
}
elseif ($venv_version -ne $installed_version) {
    Write-Status "Updating venv from $venv_version to $installed_version"
    deactivate
    $venv = Join-Path $project_root "venv"
    . $PSScriptRoot\Invoke-NonVenvPython.ps1 @('-m', 'venv', $venv, '--upgrade')
    . $PSScriptRoot\Ensure-Venv.ps1 | Out-Null
}

. $PSScriptRoot\Bootstrap.ps1 -Verbose:$Verbose

$local_db = Join-Path $project_root "back\newdjangosite.db"
if (Test-Path $local_db) {
    Write-Status "Performing database migrations"
    . $PSScriptRoot\Invoke-Manage.ps1 migrate
}
else {
    Write-Status "Creating local database"
    & $PSScriptRoot\Invoke-Manage.ps1 migrate

    Write-Status "Creating super user"
    & $PSScriptRoot\Invoke-Manage.ps1 createsuperuser
}

if (-Not $already_activated) {
    deactivate
}
