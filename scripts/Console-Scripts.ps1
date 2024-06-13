. $PSScriptRoot\Invoke-Fabric.ps1

Set-Item function:global:Invoke-Manage {
    param([switch]$Async)
    . $PSScriptRoot\Invoke-Manage.ps1 -Async:$Async @args
} -Force

Set-Item function:global:Invoke-Npm {
    param([switch]$Async, $NpmArgs)
    . $PSScriptRoot\Invoke-Npm.ps1 -Async:$Async $NpmArgs
} -Force

Set-Item function:global:Invoke-Ng {
    param([switch]$Async)
    . $PSScriptRoot\Invoke-Ng.ps1 -Async:$Async @args
} -Force

Set-Item function:global:Start-Angular {
    $npmArgs = @("start", "--", "--open")
    Invoke-Npm -Async $npmArgs
} -Force

Set-Item function:global:Start-Django {
    Invoke-Manage -Async runserver
} -Force

Set-Item function:global:Start-Server {
    Start-Angular
    Start-Django
} -Force

Set-Item function:global:Update-DevEnvironment {
    param([switch]$Verbose)
    . $PSScriptRoot\Update.ps1 -Verbose:$Verbose
} -Force

Set-Item function:global:Upgrade-Requirements {
    Push-Location $PSScriptRoot\..
    & pip-compile --upgrade --output-file=win64-py312-dev-requirements.txt '.\dev-requirements.in' '.\requirements.in'
    Pop-Location
    Write-Host 'win64-py312-dev-requirements.txt updated.'
    Write-Host 'Run pip-sync win64-py312-dev-requirements.txt to update your environment.'
}
