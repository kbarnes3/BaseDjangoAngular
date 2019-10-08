# Runs manage.py from a consistent context
# Any arguments passed into this function are passed to manage.py
param(
    [switch]$Async
)

$project_root = Split-Path $PSScriptRoot
$already_activated = . $PSScriptRoot\Ensure-Venv.ps1

$python = Join-Path $project_root "venv\Scripts\python.exe"
$backend_dir = Join-Path $project_root "back"

Push-Location $backend_dir
$args = ,"manage.py" + $args
if ($Async) {
    Start-Process $python -ArgumentList $args
}
else {
    & $python manage.py $args
}
Pop-Location

if (-Not $already_activated) {
    deactivate
}
