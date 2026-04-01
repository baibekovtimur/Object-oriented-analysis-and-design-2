param(
    [switch]$Run
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspaceDir = Split-Path -Parent $scriptDir
$drive = 'Z:'
$projectAtDrive = "$drive\\notification_facade_gui"

# Keep source path short and ASCII for Qt automoc tools.
subst $drive /d *> $null
subst $drive $workspaceDir *> $null

if (-not (Test-Path "$projectAtDrive\CMakePresets.json")) {
    throw "Failed to map $drive to workspace directory: $workspaceDir"
}

$env:PATH = "C:\msys64\ucrt64\bin;C:\msys64\usr\bin;$env:PATH"

Push-Location $projectAtDrive
try {
    cmake --preset ucrt64-ninja
    cmake --build --preset build-ucrt64

    if ($Run) {
        & "$projectAtDrive\\build\\notification_facade_gui.exe"
    }
}
finally {
    Pop-Location
}
