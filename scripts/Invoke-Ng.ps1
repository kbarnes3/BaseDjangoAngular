# Runs ng from a consistent context
# Any arguments passed into this function are passed to ng
param(
    [switch]$Async
)

$project_root = Split-Path $PSScriptRoot
$node_root = Join-Path $project_root "front"

Push-Location $node_root
if ($Async) {
    Start-Process ng.cmd -ArgumentList $args
}
else {
    & ng $args
}
Pop-Location
