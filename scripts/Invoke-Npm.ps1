# Runs NPM from a consistent context
# Any arguments passed into this function are passed to NPM
param(
    [switch]$Async,
    $NpmArgs
)

$project_root = Split-Path $PSScriptRoot
$node_root = Join-Path $project_root "front"

Push-Location $node_root
if ($Async) {
    Start-Process npm.cmd -ArgumentList $NpmArgs
} else {
    & npm.cmd @NpmArgs
}
Pop-Location
