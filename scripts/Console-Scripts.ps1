. $PSScriptRoot\Invoke-Fabric.ps1

Set-Item function:global:Invoke-Manage {
    param([switch]$Async)
    . $PSScriptRoot\Invoke-Manage.ps1 -Async:$Async @args
} -Force

Set-Item function:global:Invoke-Npm {
    . $PSScriptRoot\Invoke-Npm.ps1 @args
} -Force

Set-Item function:global:Invoke-Ng {
    param([switch]$Async)
    . $PSScriptRoot\Invoke-Ng.ps1 -Async:$Async @args
} -Force

Set-Item function:global:Start-Angular {
    $open = "--open"
    Invoke-Ng -Async serve --proxy-config proxy.conf.json $open
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
