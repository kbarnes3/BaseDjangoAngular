# Runs Fabric from a consistent context
# Any arguments passed into this function are passed to fab
Set-Item function:global:Invoke-Fabric {
    [CmdletBinding(DefaultParameterSetName="none")]
    param(
        [Parameter(Position=0, Mandatory=$true, ParameterSetName="run")]
        [string]$Hosts,
        [Parameter(ParameterSetName="run")]
        [switch]$PromptForPassphrase,
        [Parameter(ParameterSetName="run")]
        [switch]$PromptForLoginPassword,
        [Parameter(ParameterSetName="run")]
        [switch]$PromptForSudoPassword,
        [Parameter(Position=1, ValueFromRemainingArguments, ParameterSetName="run")]
        [string[]]$FabricTask,
        [Parameter(ParameterSetName="list")]
        [switch]$ListTasks
    )
    $listFunctions = $False
    $project_root = Split-Path $PSScriptRoot
    $already_activated = . $PSScriptRoot\Ensure-Venv.ps1

    $fabric = Join-Path $project_root "venv\Scripts\fab.exe"
    if ($ListTasks -or -not $Hosts) {
        $listFunctions = $True
        $fabricArgs = "--list"
    } else {
        $fabricArgs = @("--hosts", $Hosts)
        if ($PromptForPassphrase) {
            $fabricArgs += "--prompt-for-passphrase"
        }
        if ($PromptForLoginPassword) {
            $fabricArgs += "--prompt-for-login-password"
        }
        if ($PromptForSudoPassword) {
            $fabricArgs += "--prompt-for-sudo-password"
        }
        $fabricArgs += $FabricTask
    }

    Push-Location $project_root
    Start-Process $fabric -ArgumentList $fabricArgs -NoNewWindow -Wait
    Pop-Location

    if ($listFunctions) {
        Write-Host "Fabric tasks are also available as PowerShell functions:`n"
        $fabricFunctions = Get-Item function:Fabric-* | Sort-Object -Property Name
        $fabricFunctions | ForEach-Object { Write-Host "  $($_.Name)" }
        Write-Host ""
    }

    if (-Not $already_activated) {
        deactivate
    }
} -Force

Set-Item function:global:Fabric-SetupUser {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Hosts,
        [Parameter(Mandatory=$true)]
        [string]$User,
        [string]$SetPublicKeyFile,
        [switch]$DisableSudoPasswd,
        [switch]$PromptForPassphrase,
        [switch]$PromptForLoginPassword,
        [switch]$PromptForSudoPassword
    )
    $setupUserArgs = @("setup-user")
    $setupUserArgs += "--user"
    $setupUserArgs += $User
    if ($SetPublicKeyFile) {
        $setupUserArgs += "--set-public-key-file"
        $setupUserArgs += $SetPublicKeyFile
    }
    if ($DisableSudoPasswd) {
        $setupUserArgs += "--disable-sudo-passwd"
    }

    Invoke-Fabric $Hosts -PromptForPassphrase:$PromptForPassphrase -PromptForLoginPassword:$PromptForLoginPassword -PromptForSudoPassword:$PromptForSudoPassword $setupUserArgs
} -Force

Set-Item function:global:Fabric-AddAuthorizedKey {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Hosts,
        [Parameter(Mandatory=$true)]
        [string]$User,
        [Parameter(Mandatory=$true)]
        [string]$PublicKeyFile,
        [switch]$PromptForPassphrase,
        [switch]$PromptForLoginPassword,
        [switch]$PromptForSudoPassword
    )
    $addAuthorizedKeyArgs = @("add-authorized-key")
    $addAuthorizedKeyArgs += "--user"
    $addAuthorizedKeyArgs += $User
    $addAuthorizedKeyArgs += "--public-key-file"
    $addAuthorizedKeyArgs += $PublicKeyFile

    Invoke-Fabric $Hosts -PromptForPassphrase:$PromptForPassphrase -PromptForLoginPassword:$PromptForLoginPassword -PromptForSudoPassword:$PromptForSudoPassword $addAuthorizedKeyArgs
} -Force

Set-Item function:global:Fabric-DisableSshPasswords {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Hosts,
        [switch]$PromptForPassphrase,
        [switch]$PromptForLoginPassword,
        [switch]$PromptForSudoPassword
    )
    $disableSshPasswordArgs = @("disable-ssh-passwords")
    Invoke-Fabric $Hosts -PromptForPassphrase:$PromptForPassphrase -PromptForLoginPassword:$PromptForLoginPassword -PromptForSudoPassword:$PromptForSudoPassword $disableSshPasswordArgs
} -Force

Set-Item function:global:Fabric-SetupServer {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Hosts,
        [Parameter(Mandatory=$true)]
        [switch]$SetupWins,
        [switch]$PromptForPassphrase,
        [switch]$PromptForLoginPassword,
        [switch]$PromptForSudoPassword
    )
    $setupServerArgs = @("setup-server")
    if ($SetupWins) {
        $setupServerArgs += "--setup-wins"
    }

    Invoke-Fabric $Hosts -PromptForPassphrase:$PromptForPassphrase -PromptForLoginPassword:$PromptForLoginPassword -PromptForSudoPassword:$PromptForSudoPassword $setupServerArgs
} -Force

Set-Item function:global:Fabric-Deploy {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Hosts,
        [Parameter(Mandatory=$true)]
        [ValidateSet('Daily','Dev','Prod','Staging')]
        [string]$Config,
        [string]$Branch,
        [string]$SecretBranch,
        [switch]$PromptForPassphrase,
        [switch]$PromptForLoginPassword,
        [switch]$PromptForSudoPassword
    )
    $deployArgs = @("deploy")
    $deployArgs += $Config.ToLower()
    if ($Branch) {
        $deployArgs += "--branch"
        $deployArgs += $Branch
    }
    if ($SecretBranch) {
        $deployArgs += "--secret-branch"
        $deployArgs += $SecretBranch
    }

    Invoke-Fabric $Hosts -PromptForPassphrase:$PromptForPassphrase -PromptForLoginPassword:$PromptForLoginPassword -PromptForSudoPassword:$PromptForSudoPassword $deployArgs
} -Force
