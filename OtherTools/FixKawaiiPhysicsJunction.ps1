[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$KawaiiPhysicsSourcePath
)

$ErrorActionPreference = 'Stop'
$GitUrl = 'https://github.com/JasonMa0012/KawaiiPhysics_MooaToon.git'

if ([string]::IsNullOrWhiteSpace($KawaiiPhysicsSourcePath) -or
    -not [IO.Path]::IsPathRooted($KawaiiPhysicsSourcePath)) {
    throw 'KawaiiPhysicsSourcePath must be an absolute path.'
}

$SourceRoot = [IO.Path]::GetFullPath($KawaiiPhysicsSourcePath)
$SourceRootName = $SourceRoot.TrimEnd('\', '/')
if ($SourceRootName -eq ([IO.Path]::GetPathRoot($SourceRoot)).TrimEnd('\', '/')) {
    throw "Refusing to use a filesystem root as the source repository: $SourceRoot"
}

function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)

    & git -C $script:SourceRoot @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Arguments -join ' ') failed with exit code $LASTEXITCODE."
    }
}

function Test-InitializedRepository {
    if (-not (Test-Path -LiteralPath $script:SourceRoot -PathType Container)) {
        return $false
    }

    $reportedRoot = & git -C $script:SourceRoot rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -ne 0) {
        return $false
    }

    try {
        return [IO.Path]::GetFullPath(([string]($reportedRoot | Select-Object -Last 1)).Trim()) -eq $script:SourceRoot
    } catch {
        return $false
    }
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'git.exe was not found in PATH.'
}

$initialized = Test-InitializedRepository
if (-not $initialized) {
    if (Test-Path -LiteralPath $SourceRoot -PathType Leaf) {
        throw "Source path is a file, not a directory: $SourceRoot"
    }

    if (Test-Path -LiteralPath $SourceRoot -PathType Container) {
        if (@(Get-ChildItem -LiteralPath $SourceRoot -Force).Count -gt 0) {
            throw "Source path is not an initialized Git repository and is not empty: $SourceRoot"
        }
    } else {
        $sourceParent = Split-Path -Parent $SourceRoot
        if (-not (Test-Path -LiteralPath $sourceParent -PathType Container)) {
            New-Item -ItemType Directory -Path $sourceParent -Force | Out-Null
        }
    }

    Write-Host "Cloning $GitUrl to $SourceRoot"
    & git clone $GitUrl $SourceRoot
    if ($LASTEXITCODE -ne 0) {
        throw "git clone failed with exit code $LASTEXITCODE."
    }
}

Write-Host "Resetting source repository: $SourceRoot"
Invoke-Git @('reset', '--hard', 'HEAD')
Invoke-Git @('clean', '-fdx')

$sourcePluginPath = Join-Path $SourceRoot 'Plugins\KawaiiPhysics'
if (-not (Test-Path -LiteralPath $sourcePluginPath -PathType Container)) {
    throw "KawaiiPhysics plugin directory was not found after reset: $sourcePluginPath"
}

$mooatoonRoot = Split-Path -Parent $PSScriptRoot
$engineRoot = Join-Path $mooatoonRoot 'MooaToon-Engine'
$enginePluginParent = Join-Path $engineRoot 'Engine\Plugins\MooaToonThirdparty'
if (-not (Test-Path -LiteralPath $engineRoot -PathType Container)) {
    throw "Engine directory was not found: $engineRoot"
}
if (-not (Test-Path -LiteralPath $enginePluginParent -PathType Container)) {
    New-Item -ItemType Directory -Path $enginePluginParent -Force | Out-Null
}

$junctionPath = Join-Path $enginePluginParent 'KawaiiPhysics'

$existingTarget = Get-Item -LiteralPath $junctionPath -Force -ErrorAction SilentlyContinue
if ($null -ne $existingTarget) {
    Write-Host "Removing existing engine path: $junctionPath"
    if (($existingTarget.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        Remove-Item -LiteralPath $junctionPath -Force
    } else {
        Remove-Item -LiteralPath $junctionPath -Recurse -Force
    }
}

Write-Host "Creating junction: $junctionPath -> $sourcePluginPath"
New-Item -ItemType Junction -Path $junctionPath -Target $sourcePluginPath | Out-Null

$junction = Get-Item -LiteralPath $junctionPath -Force
if (($junction.Attributes -band [IO.FileAttributes]::ReparsePoint) -eq 0) {
    throw "The engine path was created, but it is not a junction: $junctionPath"
}

Write-Host 'KawaiiPhysics junction repaired successfully.'
Write-Host "Source: $sourcePluginPath"
Write-Host "Engine: $junctionPath"
